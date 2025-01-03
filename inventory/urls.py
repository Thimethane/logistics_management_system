# inventory/urls.py
from django.contrib import admin
from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('', views.home, name='home'),  # Home page (set to the root of inventory)
    path('base/', views.base, name='base'),
    path('spare-parts/', views.spare_parts_list, name='spare_parts_list'),  # Spare parts list page
    path('components/', views.component_list, name='component_list'),  # Component list page
    path('spare-parts/add/', views.add_spare_part, name='add_spare_part'),  # Add spare part page
    path('components/add/', views.add_component, name='add_component'),  # Add component page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
