from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
	# Default auth urls
	path('', include('django.contrib.auth.urls')),
	# Registration Page url
	path('register/', views.register, name='register'),
]