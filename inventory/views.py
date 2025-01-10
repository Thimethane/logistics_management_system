from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from .models import SparePart, Component, ActionLog
from .forms import SparePartForm, ComponentForm, SparePartSearchForm, ComponentSearchForm, LoginForm, ProfileUpdateForm
from .utils import ExportUtility
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def home(request):
    return render(request, 'inventory/home.html')

def base(request):
    return render(request, 'inventory/base.html')

import csv
from django.http import HttpResponse
from .models import Component, SparePart
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def export_csv_view(request):
    # Get the type of data being requested (either 'components' or 'spare_parts')
    data_type = request.GET.get('data_type', '')
    search_query = request.GET.get('search_query', '')

    # Determine which model to use (Component or SparePart)
    if data_type == 'components':
        data = Component.objects.all()
        model_name = 'Component'
        file_name = 'components.csv'
    elif data_type == 'spare_parts':
        data = SparePart.objects.all()
        model_name = 'SparePart'
        file_name = 'spare_parts.csv'
    else:
        return HttpResponse("Invalid data type.", status=400)

    # Filter data based on the search query
    if search_query:
        data = data.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Pagination setup
    page_number = request.GET.get('page', 1)
    paginator = Paginator(data, 10)  # 10 items per page
    page_obj = paginator.get_page(page_number)

    # Create the HTTP response with content type 'text/csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Dynamically fetch the field names from the model
    field_names = [field.name for field in data.model._meta.get_fields()]

    # Write the header row (column names)
    writer.writerow(field_names)

    # Write each object as a row in the CSV
    for item in page_obj:
        row = [getattr(item, field) for field in field_names]
        writer.writerow(row)

    return response

@login_required
def export_pdf_view(request):
    # Get the export_type parameter (either 'spareparts' or 'components')
    export_type = request.GET.get('export_type', '').lower()

    # Check if export_type is missing or invalid
    if not export_type:
        return HttpResponse("Error: Missing 'export_type' parameter. Please specify 'spareparts' or 'components'.", status=400)

    if export_type not in ['spareparts', 'components']:
        return HttpResponse(f"Error: Invalid 'export_type' value. Expected 'spareparts' or 'components', but got '{export_type}'.", status=400)

    # Determine which model to use based on the export type
    if export_type == 'spareparts':
        items = SparePart.objects.all()
        filename = "spare_parts.pdf"
        title = "Spare Parts Report"
        model = SparePart
    elif export_type == 'components':
        items = Component.objects.all()
        filename = "components.pdf"
        title = "Components Report"
        model = Component

    # Create the HTTP response with content type 'application/pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create the PDF object and set up the page size
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Standard page size

    y_position = height - 50  # Start from the top of the page

    # Write title
    p.setFont("Helvetica", 16)
    p.drawString(100, y_position, title)
    y_position -= 30  # Move down for the next section

    # Set font for content
    p.setFont("Helvetica", 10)

    # Write the header dynamically based on model field names
    fields = [field.name for field in model._meta.get_fields()]
    header = ", ".join(fields)
    p.drawString(100, y_position, header)
    y_position -= 15  # Move down for the data

    # Write each item's field values dynamically
    for item in items:
        row = ", ".join(str(getattr(item, field)) for field in fields)
        p.drawString(100, y_position, row)
        y_position -= 15  # Move down for the next row

        # Check if we need to create a new page if the content goes off the page
        if y_position < 50:
            p.showPage()  # Start a new page
            y_position = height - 50  # Reset the position

    # Save the PDF and return the response
    p.showPage()
    p.save()

    return response

@login_required
@permission_required('inventory.can_view_sparepart', raise_exception=True)
def spare_parts_list(request):
    form = SparePartSearchForm(request.GET)
    spare_parts = SparePart.objects.all()

    if not spare_parts.exists():
        return HttpResponse("No spare parts found.", status=404)

    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        if query:
            spare_parts = spare_parts.filter(
                Q(name__icontains=query) |
                Q(serial_number__icontains=query) |
                Q(location__icontains=query)
            )

    # Sorting parameters
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')

    valid_sort_fields = ['name', 'created_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    if order not in ['asc', 'desc']:
        order = 'asc'

    # Apply sorting based on selected field and order
    if sort_by == 'name':
        spare_parts = spare_parts.order_by('name' if order == 'asc' else '-name')
    elif sort_by == 'created_at':
        spare_parts = spare_parts.order_by('created_at' if order == 'asc' else '-created_at')

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(spare_parts, 10)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        return HttpResponse(f"Error in pagination: {str(e)}", status=400)

    # Export options
    if request.GET.get('export_csv'):
        try:
            response = HttpResponse(ExportUtility.export_to_csv(spare_parts), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="spare_parts.csv"'
            return response
        except ValueError as e:
            return HttpResponse(f"Export Error: {str(e)}", status=400)

    if request.GET.get('export_pdf'):
        try:
            response = ExportUtility.download_pdf(spare_parts, file_name="spare_parts.pdf")
            return response
        except Exception as e:
            return HttpResponse(f"Export Error: {str(e)}", status=400)

    # Rendering the template with the context
    return render(
        request,
        'inventory/spare_parts_list.html',
        {
            'spare_parts': page_obj,
            'search_query': form.cleaned_data.get('query', ''),
            'form': form,
            'page_obj': page_obj,
            'sort_by': sort_by,
            'order': order,
        }
    )

@login_required
@permission_required('inventory.can_view_component', raise_exception=True)
def component_list(request):
    # Get query parameter or default to empty string
    query = request.GET.get('query', '').strip()
    
    # Initialize the query filter
    components = Component.objects.all()

    # Handling search query if present
    if query:
        components = components.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Sorting parameters
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')

    valid_sort_fields = ['name', 'created_at']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    if order not in ['asc', 'desc']:
        order = 'asc'

    # Apply sorting based on selected field and order
    if sort_by == 'name':
        components = components.order_by('name' if order == 'asc' else '-name')
    elif sort_by == 'created_at':
        components = components.order_by('created_at' if order == 'asc' else '-created_at')

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(components, 10)
    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        return HttpResponse(f"Error in pagination: {str(e)}", status=400)

    # Handle export request
    export_csv = request.GET.get('export_csv', False)
    export_pdf = request.GET.get('export_pdf', False)

    # Process CSV export
    if export_csv:
        try:
            response = HttpResponse(ExportUtility.export_to_csv(components), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="components.csv"'
            return response
        except ValueError as e:
            return HttpResponse(f"Export Error: {str(e)}", status=400)

    # Process PDF export
    if export_pdf:
        try:
            response = ExportUtility.download_pdf(components, file_name="components.pdf")
            return response
        except Exception as e:
            return HttpResponse(f"Export Error: {str(e)}", status=400)

    # Rendering the template with the context
    return render(
        request,
        'inventory/component_list.html',
        {
            'components': page_obj,
            'search_query': query,
            'page_obj': page_obj,
            'sort_by': sort_by,
            'order': order,
        }
    )

def edit_component(request, id):
    component = get_object_or_404(Component, id=id)
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            messages.success(request, 'Component updated successfully!')
            return redirect('component_list')
    else:
        form = ComponentForm(instance=component)

    return render(request, 'inventory/edit_component.html', {'form': form, 'component': component})

def delete_component(request, id):
    component = get_object_or_404(Component, id=id)
    
    if request.method == 'POST':
        component.delete()
        messages.success(request, 'Component deleted successfully!')
        return redirect('component_list')
    
    return render(request, 'inventory/confirm_delete.html', {'component': component})

@login_required
@permission_required('inventory.add_sparepart', raise_exception=True)
def add_spare_part(request):
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
            messages.success(request, 'Spare part updated successfully!')
            return redirect('spare_parts_list')
    else:
        form = SparePartForm(instance=spare_part)

    return render(request, 'inventory/edit_spare_part.html', {'form': form, 'spare_part': spare_part})

def export_spareparts_csv(request):
    spare_parts = SparePart.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="spare_parts.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Serial Number', 'Location', 'Condition', 'Repair History'])

    for part in spare_parts:
        writer.writerow([
            part.id,
            part.name,
            part.serial_number,
            part.location,
            part.get_condition_display(),
            part.repair_history,
        ])

    return response

def delete_spare_part(request, id):
    spare_part = get_object_or_404(SparePart, id=id)
    spare_part.delete()
    messages.success(request, 'Spare part deleted successfully!')
    return redirect('spare_parts_list')

@login_required
@permission_required('inventory.add_component', raise_exception=True)
def add_component(request):
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
    return user.groups.filter(name='Admin').exists()

def log_action(user, action_type, model_affected, item_id):
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
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'inventory/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('home'))  # Redirect to the landing page or another page
    else:
        return HttpResponse(status=405)  # Method Not Allowed for GET requests

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

@login_required
def profile_view(request):
    user = request.user
    profile_form = UserProfileForm(instance=user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
    return render(request, 'inventory/profile.html', {'profile_form': profile_form})
