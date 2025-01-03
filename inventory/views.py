from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import Group
from .models import SparePart, Component, ActionLog, ExportUtility
from .forms import SparePartForm, ComponentForm, SparePartSearchForm
from .forms import LoginForm  # Assuming you have a form for login
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms import ModelForm
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import ExportUtility
from django.shortcuts import get_list_or_404

def home(request):
    return render(request, 'inventory/home.html')

def base(request):
    return render(request, 'inventory/base.html')

@login_required
@permission_required('inventory.view_sparepart', raise_exception=True)
def spare_parts_list(request):
    """
    View to display, search, sort, and export spare parts.
    Handles search query, sorting, pagination, and export options (CSV/PDF).
    """
    # Initialize the search form with GET data
    form = SparePartSearchForm(request.GET)
    spare_parts = SparePart.objects.all()

    # Handle search query
    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        if query:
            # Debugging the search query
            print(f"Search Query: {query}")  # For debugging
            spare_parts = spare_parts.filter(
                Q(name__icontains=query) |
                Q(serial_number__icontains=query) |
                Q(location__icontains=query)
            )

    # Handle sorting by name or date_received
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    # Debugging the sorting parameters
    print(f"Sort By: {sort_by}, Order: {order}")  # For debugging
    
    if sort_by == 'name':
        spare_parts = spare_parts.order_by('name' if order == 'asc' else '-name')
    elif sort_by == 'date_received':
        spare_parts = spare_parts.order_by('created_at' if order == 'asc' else '-created_at')

    # Pagination setup
    page_number = request.GET.get('page', 1)  # Default to first page
    paginator = Paginator(spare_parts, 10)  # 10 spare parts per page
    page_obj = paginator.get_page(page_number)

    # Debugging the count of filtered and sorted spare parts
    print(f"Total spare parts after filtering and sorting: {spare_parts.count()}")  # For debugging

    # Handle export requests (CSV or PDF)
    if request.GET.get('export_csv'):
        response = HttpResponse(ExportUtility.export_to_csv(spare_parts), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="spare_parts.csv"'
        return response

    if request.GET.get('export_pdf'):
        response = HttpResponse(ExportUtility.export_to_pdf(spare_parts), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="spare_parts.pdf"'
        return response

    # Render the spare parts list page with pagination, search query, and spare parts
    return render(
        request,
        'inventory/spare_parts_list.html',
        {
            'spare_parts': page_obj,  # Paginated spare parts
            'search_query': form.cleaned_data.get('query', ''),  # Search query
            'form': form,  # The search form
            'page_obj': page_obj,  # Pagination object
            'sort_by': sort_by,  # Current sorting option
            'order': order,  # Current sort order
        }
    )

@login_required
def component_list(request):
    """
    View to display a list of components with search, pagination, and export functionality.
    Handles:
    - Searching components by name or description
    - Paginating the components list
    - Exporting the list as CSV or PDF
    """
    # Handle the search query from the GET request
    search_query = request.GET.get('search_query', '')
    components = Component.objects.all()

    # Apply search filter if search query is provided
    if search_query:
        components = components.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Handle pagination: Get the current page number, defaulting to 1
    page_number = request.GET.get('page', 1)
    paginator = Paginator(components, 10)  # 10 components per page
    page_obj = paginator.get_page(page_number)

    # Handle export requests (CSV or PDF)
    if request.GET.get('export_csv'):
        # Export to CSV
        response = HttpResponse(ExportUtility.export_to_csv(components), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="components.csv"'
        return response

    if request.GET.get('export_pdf'):
        # Export to PDF
        response = HttpResponse(ExportUtility.export_to_pdf(components), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="components.pdf"'
        return response

    # Render the component list page with pagination, search query, and components
    return render(
        request,
        'inventory/component_list.html',
        {
            'components': page_obj,  # Paginated components for the current page
            'search_query': search_query,  # The search query entered by the user
            'page_obj': page_obj,  # Pagination object for the template
        }
    )
    
def edit_component(request, id):
    component = get_object_or_404(Component, id=id)
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()  # Save the updated component
            return redirect('component_list')  # Redirect to the component list page after saving
    else:
        form = ComponentForm(instance=component)

    return render(request, 'inventory/edit_component.html', {'form': form, 'component': component})

def delete_component(request, id):
    component = get_object_or_404(Component, id=id)
    
    if request.method == 'POST':
        component.delete()  # Delete the component
        return redirect('component_list')  # Redirect to the component list after deletion
    
    return render(request, 'inventory/confirm_delete.html', {'component': component})

@login_required
@permission_required('inventory.add_sparepart', raise_exception=True)
def add_spare_part(request):
    """
    View to add a new spare part with transaction handling and action logging.
    """
    if request.method == 'POST':
        form = SparePartForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                new_spare_part = form.save()
                log_action(request.user, 'add', 'SparePart', new_spare_part.id)
            messages.success(request, 'Spare part added successfully!')
            return redirect('spare_parts_list')
    else:
        form = SparePartForm()
    return render(request, 'inventory/add_spare_part.html', {'form': form})

def edit_spare_part(request, id):
    spare_part = get_object_or_404(SparePart, id=id)

    if request.method == 'POST':
        form = SparePartForm(request.POST, instance=spare_part)
        if form.is_valid():
            form.save()
            # Optionally, you can redirect to the spare parts list page or another page after saving
            return redirect('spare_parts_list')  # Adjust this URL name as needed
    else:
        form = SparePartForm(instance=spare_part)

    return render(request, 'inventory/edit_spare_part.html', {'form': form, 'spare_part': spare_part})

def delete_spare_part(request, id):
    spare_part = get_object_or_404(SparePart, id=id)
    spare_part.delete()
    return redirect('spare_parts_list')



@login_required
@permission_required('inventory.add_component', raise_exception=True)
def add_component(request):
    """
    View to add a new component.
    """
    if request.method == 'POST':
        form = ComponentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Component added successfully!')
            return redirect('component_list')
    else:
        form = ComponentForm()
    return render(request, 'inventory/add_component.html', {'form': form})


def register(request):
    """
    View to register a new user and log them in immediately.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('spare_parts_list')
    else:
        form = UserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})


def check_role(user):
    """
    Utility function to check if the user belongs to the 'Admin' group.
    """
    return user.groups.filter(name='Admin').exists()


def log_action(user, action_type, model_affected, item_id):
    """
    Utility function to log user actions into the ActionLog model.
    """
    ActionLog.objects.create(
        user=user,
        action_type=action_type,
        model_affected=model_affected,
        item_id=item_id
    )


@login_required
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after login
    else:
        form = LoginForm()
    return render(request, 'inventory/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout


# Custom form for updating user profile
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


@login_required
def profile_view(request):
    user = request.user

    # Initialize forms
    profile_form = UserProfileForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        # Handle profile update
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')

        # Handle password change
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Prevent logout after password change
                messages.success(request, 'Your password has been changed!')
                return redirect('profile')

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'inventory/profile.html', context)


def component_list(request):
    components = Component.objects.all()
    paginator = Paginator(components, 10)  # Show 10 components per page
    page_number = request.GET.get('page')
    components_page = paginator.get_page(page_number)
    return render(request, 'inventory/component_list.html', {'components': components_page})

def spare_parts_list(request):
    spare_parts = SparePart.objects.all()
    paginator = Paginator(spare_parts, 10)  # Show 10 spare parts per page
    page_number = request.GET.get('page')
    spare_parts_page = paginator.get_page(page_number)
    return render(request, 'inventory/spare_parts_list.html', {'spare_parts': spare_parts_page})

def export_components(request):
    components = Component.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="components.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Description', 'Classification'])
    for component in components:
        writer.writerow([component.id, component.name, component.description, component.classification])
    
    return response

def export_spare_parts(request):
    spare_parts = SparePart.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="spare_parts.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Description', 'Classification'])
    for spare_part in spare_parts:
        writer.writerow([spare_part.id, spare_part.name, spare_part.description, spare_part.classification])
    
    return response


# inventory/views.py

def export_spare_parts_csv(request):
    """
    View to export spare parts as a downloadable CSV.
    """
    spare_parts = get_list_or_404(SparePart)
    return ExportUtility.export_to_csv(spare_parts, filename="spare_parts.csv")

def export_spare_parts_pdf(request):
    """
    View to export spare parts as a downloadable PDF.
    """
    spare_parts = get_list_or_404(SparePart)
    return ExportUtility.export_to_pdf(spare_parts, filename="spare_parts.pdf")

def export_components_csv(request):
    """
    View to export components as a downloadable CSV.
    """
    components = get_list_or_404(Component)
    return ExportUtility.export_to_csv(components, filename="components.csv")

def export_components_pdf(request):
    """
    View to export components as a downloadable PDF.
    """
    components = get_list_or_404(Component)
    return ExportUtility.export_to_pdf(components, filename="components.pdf")

