from django.urls import path

from . import views

# This is the main index page of the site
# The first page that is loaded when the site is loaded

app_name = 'book_keeping'
urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.events, name='events'),
    path('new_event/', views.new_event, name='new_event'),
    path('add_vol/', views.add_vol, name='add_vol'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('donate/', views.donate_event, name='donate_event'),
]
