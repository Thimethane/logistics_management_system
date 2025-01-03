from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import Group
from .models import SparePart, Component, ActionLog
from .forms import SparePartForm, ComponentForm, SparePartSearchForm

def home(request):
    return render(request, 'inventory/home.html')


@login_required
@permission_required('inventory.view_sparepart', raise_exception=True)
def spare_parts_list(request):
    """
    View to display and search spare parts.
    """
    form = SparePartSearchForm(request.GET)
    spare_parts = SparePart.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        if query:
            spare_parts = spare_parts.filter(name__icontains=query)

    return render(request, 'inventory/spare_parts_list.html', {'spare_parts': spare_parts, 'form': form})

@login_required
def component_list(request):
    """
    View to display a list of components.
    """
    components = Component.objects.all()
    return render(request, 'inventory/component_list.html', {'components': components})

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
            return redirect('spare_parts_list')
    else:
        form = SparePartForm()
    return render(request, 'inventory/add_spare_part.html', {'form': form})

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
