from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Login / Logout — using Django's built-in auth views
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard — home page
    path('', include('dashboard.urls')),

    # Clients app routes under /clients/
    path('clients/', include('clients.urls')),

    # Subscriptions app routes under /subscriptions/
    path('subscriptions/', include('subscriptions.urls')),
]