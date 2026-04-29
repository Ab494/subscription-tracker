from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from clients.models import Client
from subscriptions.models import Subscription


@login_required
def dashboard(request):
    """
    Main dashboard view showing an overview of all
    clients and subscription statuses.
    """
    today = timezone.now().date()
    soon = today + timedelta(days=7)

    # Total number of clients registered
    total_clients = Client.objects.count()

    # All subscriptions for computing status counts
    all_subscriptions = Subscription.objects.select_related('client').all()

    # Active — expiry date is today or in the future
    active_subscriptions = all_subscriptions.filter(expiry_date__gte=today)

    # Expired — expiry date is in the past
    expired_subscriptions = all_subscriptions.filter(expiry_date__lt=today)

    # Expiring within the next 7 days (but not yet expired)
    expiring_soon = all_subscriptions.filter(
        expiry_date__gte=today,
        expiry_date__lte=soon
    )

    # Unpaid subscriptions regardless of expiry
    unpaid_subscriptions = all_subscriptions.filter(payment_status='unpaid')

    return render(request, 'dashboard/dashboard.html', {
        'total_clients': total_clients,
        'active_count': active_subscriptions.count(),
        'expired_count': expired_subscriptions.count(),
        'expiring_soon_count': expiring_soon.count(),
        'unpaid_count': unpaid_subscriptions.count(),
        'expiring_soon_list': expiring_soon,  # For listing them on dashboard
        'today': today,
        'soon': soon,
    })