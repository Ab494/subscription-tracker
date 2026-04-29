from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    """
    Form for creating and editing a client.
    Uses ModelForm to auto-generate fields from the Client model.
    """

    class Meta:
        model = Client
        # Fields to include in the form
        fields = ['name', 'phone_number', 'email', 'business_name', 'status']

        # Add Bootstrap styling and placeholders to each field
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 0712345678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Business or company name'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }