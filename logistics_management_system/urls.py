"""logistics_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# logistics_management_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory import views as inventory_views  # Correctly import views from inventory app


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin path
    path('', inventory_views.home, name='home'),  # Root URL mapped to home view
    path('inventory/', include('inventory.urls')),  # Including the inventory app URLs
    path('register/', inventory_views.register, name='register'),  # Register URL
    path('accounts/', include('django.contrib.auth.urls')),
]
