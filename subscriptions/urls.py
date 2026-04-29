from django.urls import path
from . import views

# All URL patterns for the subscriptions app
urlpatterns = [
    # List all subscriptions with optional filter
    path('', views.subscription_list, name='subscription_list'),

    # Add a subscription (optionally pre-linked to a client)
    path('add/', views.subscription_create, name='subscription_create'),
    path('add/client/<int:client_pk>/', views.subscription_create, name='subscription_create_for_client'),

    # Edit an existing subscription
    path('<int:pk>/edit/', views.subscription_edit, name='subscription_edit'),

    # Delete a subscription
    path('<int:pk>/delete/', views.subscription_delete, name='subscription_delete'),
     # Export all subscriptions as CSV
    path('export/csv/', views.export_subscriptions_csv, name='export_subscriptions_csv'),
]