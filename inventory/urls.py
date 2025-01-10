from django.urls import path
from . import views

urlpatterns = [
    # Home and Base Views
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),

    # Spare Parts Views
    path('spare-parts/', views.spare_parts_list, name='spare_parts_list'),
    path('spare-parts/add/', views.add_spare_part, name='add_spare_part'),
    path('spare-parts/edit/<int:id>/', views.edit_spare_part, name='edit_spare_part'),
    path('spare-parts/delete/<int:id>/', views.delete_spare_part, name='delete_spare_part'),

    # Component Views
    path('components/', views.component_list, name='component_list'),
    path('components/add/', views.add_component, name='add_component'),
    path('components/edit/<int:id>/', views.edit_component, name='edit_component'),
    path('components/delete/<int:id>/', views.delete_component, name='delete_component'),

    # User Authentication Views
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),    

    # User Profile View
    path('profile/', views.profile_view, name='profile'),
    
    path('export-csv/', views.export_csv_view, name='export_csv_view'),
    path('spare-parts/export/pdf/', views.export_pdf_view, name='export_pdf_view'),
]
