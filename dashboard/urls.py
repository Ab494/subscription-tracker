from django.urls import path
from . import views

urlpatterns = [
    # Dashboard home
    path('', views.dashboard, name='dashboard'),
]