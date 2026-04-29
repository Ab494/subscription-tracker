from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    """
    Form for creating and editing a subscription record.
    Linked to a specific client via ForeignKey.
    """

    class Meta:
        model = Subscription
        # Exclude auto-managed fields
        fields = ['client', 'start_date', 'expiry_date', 'amount_paid', 'payment_status', 'notes']

        # Add Bootstrap styling and appropriate input types
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Renders native date picker in browser
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'amount_paid': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # Compact textarea
                'placeholder': 'Any additional notes...'
            }),
        }