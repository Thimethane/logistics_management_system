from django import forms
from .models import SparePart, Component
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings

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
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class SparePartSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')


class ComponentSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search Components',
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or description', 'class': 'form-control'})
    )

    def clean_query(self):
        query = self.cleaned_data.get('query', '')
        return query.strip() if query else ''

