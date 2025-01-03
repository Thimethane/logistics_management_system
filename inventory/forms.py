from django import forms
from .models import SparePart, Component

class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['name', 'serial_number', 'condition', 'location', 'repair_history']

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'description', 'quantity', 'status']


class SparePartSearchForm(forms.Form):
    query = forms.CharField(label='Search Spare Parts', max_length=100, required=False)
