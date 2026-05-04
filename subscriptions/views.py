from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Subscription
from .forms import SubscriptionForm
import csv
from django.http import HttpResponse


@login_required
def subscription_list(request):
    """
    Display all subscriptions with optional filter by payment
    status or subscription status (active, expired, expiring soon).
    """
    subscriptions = Subscription.objects.select_related('client').all()

    # Get both filter values from URL params
    payment_filter = request.GET.get('payment', '')
    status_filter = request.GET.get('status', '')

    today = timezone.now().date()
    soon = today + timedelta(days=7)

    # Filter by payment status if provided
    if payment_filter:
        subscriptions = subscriptions.filter(payment_status=payment_filter)

    # Filter by subscription status if provided
    if status_filter == 'active':
        # Active — expiry date beyond the 7 day warning window
        subscriptions = subscriptions.filter(expiry_date__gt=soon)
    elif status_filter == 'expired':
        # Expired — expiry date is in the past
        subscriptions = subscriptions.filter(expiry_date__lt=today)
    elif status_filter == 'expiring_soon':
        # Expiring soon — within next 7 days but not yet expired
        subscriptions = subscriptions.filter(
            expiry_date__gte=today,
            expiry_date__lte=soon
        )

    return render(request, 'subscriptions/subscription_list.html', {
        'subscriptions': subscriptions,
        'payment_filter': payment_filter,
        'status_filter': status_filter,
        'today': today,
        'soon': soon,
    })

@login_required
def subscription_create(request, client_pk=None):
    """
    Create a new subscription.
    Optionally pre-select a client if coming from client detail page.
    """
    initial = {}

    if client_pk:
        # Pre-fill the client field if client_pk is provided in URL
        initial['client'] = client_pk

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(initial=initial)

    return render(request, 'subscriptions/subscription_form.html', {
        'form': form,
        'title': 'Add Subscription',
    })


@login_required
def subscription_edit(request, pk):
    """
    Edit an existing subscription record.
    """
    subscription = get_object_or_404(Subscription, pk=pk)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=subscription)

    return render(request, 'subscriptions/subscription_form.html', {
        'form': form,
        'title': 'Edit Subscription',
        'subscription': subscription,
    })


@login_required
def subscription_delete(request, pk):
    """
    Confirm and delete a subscription record.
    """
    subscription = get_object_or_404(Subscription, pk=pk)

    if request.method == 'POST':
        client_pk = subscription.client.pk
        subscription.delete()
        # Redirect back to the client's detail page after deletion
        return redirect('client_detail', pk=client_pk)

    return render(request, 'subscriptions/subscription_confirm_delete.html', {
        'subscription': subscription,
    })




@login_required
def export_subscriptions_csv(request):
    """
    Export all subscriptions as a downloadable CSV file.
    Uses Django's HttpResponse with text/csv content type.
    """
    # Set response as a CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscriptions.csv"'

    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'Client Name',
        'Business Name',
        'Phone Number',
        'Email',
        'Start Date',
        'Expiry Date',
        'Amount Paid (KES)',
        'Payment Status',
        'Subscription Status',
        'Notes',
    ])

    # Fetch all subscriptions with related client data
    subscriptions = Subscription.objects.select_related('client').all()

    for sub in subscriptions:
        # Determine human-readable subscription status
        if sub.is_expiring_soon:
            status = 'Expiring Soon'
        elif sub.is_active:
            status = 'Active'
        else:
            status = 'Expired'

        # Write one row per subscription
        writer.writerow([
            sub.client.name,
            sub.client.business_name,
            sub.client.phone_number,
            sub.client.email,
            sub.start_date,
            sub.expiry_date,
            sub.amount_paid,
            sub.get_payment_status_display(),  # Returns 'Paid', 'Unpaid', 'Partial'
            status,
            sub.notes or '',
        ])

    return response