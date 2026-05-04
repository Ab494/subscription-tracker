from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    """
    Form for creating and editing a subscription record.
    Includes custom validation for date logic and amount.
    """

    class Meta:
        model = Subscription
        fields = ['client', 'start_date', 'expiry_date', 'amount_paid', 'payment_status', 'notes']

        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
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
                'rows': 3,
                'placeholder': 'Any additional notes...'
            }),
        }

    def clean_amount_paid(self):
        """Ensure amount paid is not negative."""
        amount = self.cleaned_data.get('amount_paid')
        if amount is not None and amount < 0:
            raise forms.ValidationError("Amount paid cannot be negative.")
        return amount

    def clean(self):
        """Ensure expiry date is not earlier than start date."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        expiry_date = cleaned_data.get('expiry_date')

        if start_date and expiry_date:
            if expiry_date < start_date:
                raise forms.ValidationError(
                    "Expiry date cannot be earlier than the start date."
                )
        return cleaned_data