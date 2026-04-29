from django.urls import path
from . import views

# All URL patterns for the clients app
urlpatterns = [
    # List all clients
    path('', views.client_list, name='client_list'),

    # View a single client's details
    path('<int:pk>/', views.client_detail, name='client_detail'),

    # Add a new client
    path('add/', views.client_create, name='client_create'),

    # Edit an existing client
    path('<int:pk>/edit/', views.client_edit, name='client_edit'),

    # Delete a client
    path('<int:pk>/delete/', views.client_delete, name='client_delete'),
]