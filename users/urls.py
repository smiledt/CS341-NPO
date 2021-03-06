from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    # Auth urls
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='users/login.html')
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='users/logged_out.html')
    ),
    path('', include('django.contrib.auth.urls')),
    # Registration Page url
    path('register/', views.register, name='register'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('list_accounts/', views.list_accounts, name='list_accounts')
]
