# inventory/urls.py
from django.contrib import admin
from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('', views.home, name='home'),  # Home page (set to the root of inventory)
    path('spare-parts/', views.spare_parts_list, name='spare_parts_list'),  # Spare parts list page
    path('components/', views.component_list, name='component_list'),  # Component list page
    path('spare-parts/add/', views.add_spare_part, name='add_spare_part'),  # Add spare part page
    path('components/add/', views.add_component, name='add_component'),  # Add component page
]
