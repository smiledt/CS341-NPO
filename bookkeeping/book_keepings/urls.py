from django.urls import path

from . import views

app_name = 'book_keepings'
urlpatterns = [
	path('', views.index, name='index'),
	path('events/', views.events, name= 'events' ),
	path('new_event/', views.new_event, name='new_event'),
]