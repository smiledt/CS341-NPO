from django import forms
from .models import Event, Donation


class EventForm(forms.ModelForm):
    # Custom validation goes here
    class Meta:
        model = Event
        fields = ['name', 'date_of_event', 'start_time', 'end_time',
                  'location', 'description', 'num_volunteers_total']


class DonationForm(forms.ModelForm):
    # TODO: Add custom validation
    class Meta:
        model = Donation
        fields = ['donation', 'donation_type']
