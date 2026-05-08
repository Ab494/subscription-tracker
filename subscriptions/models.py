from django.db import models
from django.utils import timezone
from datetime import timedelta
from clients.models import Client


# Payment status options for a subscription
PAYMENT_STATUS_CHOICES = [
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
    ('partial', 'Partial'),
]


class Subscription(models.Model):
    """
    Tracks a subscription record linked to a specific client.
    Includes payment info, dates, and computed status properties.
    """

    # Link to the client this subscription belongs to
    # Deleting a client will also delete all their subscriptions
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    # Subscription date range
    start_date = models.DateField()
    expiry_date = models.DateField()

    # Payment details
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    # Optional notes about this subscription
    notes = models.TextField(blank=True, null=True)

    # Auto-set when the subscription record is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} — expires {self.expiry_date}"

    @property
    def is_active(self):
      """
      Returns True only if subscription is active
      and not within the 7 day expiry warning window."""
      today = timezone.now().date()
      soon = today + timedelta(days=7)
      return self.expiry_date > soon

    @property
    def is_expired(self):
        """Returns True if the expiry date is in the past."""
        return self.expiry_date < timezone.now().date()

    @property
    def is_expiring_soon(self):
        """Returns True if the subscription expires within the next 7 days."""
        today = timezone.now().date()
        return today <= self.expiry_date <= today + timedelta(days=7)

    class Meta:
        # Show most recently created subscriptions first
        ordering = ['-created_at']