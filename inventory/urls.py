from django.contrib import admin
from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Base Template (example route to view common layout if required)
    path('base/', views.base, name='base'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # User Profile and Settings
    path('profile/', views.profile_view, name='profile'),

    # Spare Parts Management
    path('spare-parts/', views.spare_parts_list, name='spare_parts_list'),  # List spare parts
    path('spare-parts/add/', views.add_spare_part, name='add_spare_part'),  # Add spare part
    path('edit/<int:id>/', views.edit_spare_part, name='edit_spare_part'),
    path('delete/<int:id>/', views.delete_spare_part, name='delete_spare_part'),

    # Spare Parts Export
    path('export/spare-parts/', views.export_spare_parts, name='export_spare_parts'),  # Export main view
    path('export/spare-parts/csv/', views.export_spare_parts_csv, name='export_spare_parts_csv'),  # Export CSV
    path('export/spare-parts/pdf/', views.export_spare_parts_pdf, name='export_spare_parts_pdf'),  # Export PDF

    # Component Management
    path('components/', views.component_list, name='component_list'),  # List components
    path('components/add/', views.add_component, name='add_component'),# Add component
    path('edit/<int:id>/', views.edit_component, name='edit_component'),
    path('delete/<int:id>/', views.delete_component, name='delete_component'),

    # Component Export
    path('export/components/', views.export_components, name='export_components'),  # Export main view
    path('export/components/csv/', views.export_components_csv, name='export_components_csv'),  # Export CSV
    path('export/components/pdf/', views.export_components_pdf, name='export_components_pdf'),  # Export PDF

    # Admin Dashboard
    path('admin/', admin.site.urls),  # Django admin site
]
