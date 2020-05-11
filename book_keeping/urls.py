from django.urls import path

from . import views

# This is the main index page of the site
# The first page that is loaded when the site is loaded

app_name = 'book_keeping'
urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.events, name='events'),
    path('admin_events/', views.admin_events, name='admin_events'),
    path('new_event/', views.new_event, name='new_event'),
    path('add_vol/', views.add_vol, name='add_vol'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('summary/', views.summary_report, name='summary_report'),
    path('unvolunteer/', views.unvolunteer_event, name='unvolunteer_event'),
    path('donate/', views.donate, name='donate'),
    path('standard_index/', views.standard_index, name='standard_index'),
    path('unvolunteer_list/', views.unvolunteer_list, name='unvolunteer_list')
]
