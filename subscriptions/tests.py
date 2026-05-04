from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from clients.models import Client
from .models import Subscription


class SubscriptionStatusTests(TestCase):
    """
    Tests for the subscription status logic —
    is_active, is_expired, and is_expiring_soon properties.
    """

    def setUp(self):
        """
        Create a reusable test client object before each test.
        This runs automatically before every test method.
        """
        self.client_obj = Client.objects.create(
            name="Test Client",
            phone_number="0712345678",
            email="test@example.com",
            business_name="Test Business",
            status="active"
        )

    def test_active_subscription(self):
        """
        A subscription with an expiry date 30 days in the future
        should be active, not expired, and not expiring soon.
        """
        sub = Subscription.objects.create(
            client=self.client_obj,
            start_date=timezone.now().date(),
            expiry_date=timezone.now().date() + timedelta(days=30),
            amount_paid=1000,
            payment_status='paid'
        )
        self.assertTrue(sub.is_active)
        self.assertFalse(sub.is_expired)
        self.assertFalse(sub.is_expiring_soon)

    def test_expired_subscription(self):
        """
        A subscription with an expiry date 10 days in the past
        should be expired and not active.
        """
        sub = Subscription.objects.create(
            client=self.client_obj,
            start_date=timezone.now().date() - timedelta(days=60),
            expiry_date=timezone.now().date() - timedelta(days=10),
            amount_paid=1000,
            payment_status='paid'
        )
        self.assertTrue(sub.is_expired)
        self.assertFalse(sub.is_active)
        self.assertFalse(sub.is_expiring_soon)

    def test_expiring_soon_subscription(self):
        """
        A subscription expiring in 5 days should flag as
        expiring soon and still be considered active.
        """
        sub = Subscription.objects.create(
            client=self.client_obj,
            start_date=timezone.now().date() - timedelta(days=25),
            expiry_date=timezone.now().date() + timedelta(days=5),
            amount_paid=500,
            payment_status='unpaid'
        )
        self.assertTrue(sub.is_expiring_soon)
        self.assertTrue(sub.is_active)
        self.assertFalse(sub.is_expired)