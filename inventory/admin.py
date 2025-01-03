from django.contrib import admin
from .models import SparePart, Component  # Import your models

# Register your models to make them appear in the admin panel
admin.site.register(SparePart)
admin.site.register(Component)
