from django.db import models


# Choices for client status
STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]


class Client(models.Model):
    """
    Represents a business client being tracked
    in the subscription system.
    """

    # Basic client information
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  # Each client must have a unique email
    business_name = models.CharField(max_length=200)

    # Client account status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Auto-managed timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save

    def __str__(self):

        
        # Human-readable representation used in admin and dropdowns
        return f"{self.name} — {self.business_name}"

    class Meta:
        # Show newest clients first
        ordering = ['-created_at']