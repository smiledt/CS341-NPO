from django import forms
from .models import Event, Donation, VolunteerEvent

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'date_of_event', 'start_time', 'end_time', 'location', 'description', 'num_volunteers_total']

class DeleteEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name']

class DonationForm(forms.ModelForm):
	class Meta:
		model = Donation
		fields = ['username', 'donation', 'donation_types', 'name_event']

class SummaryForm(forms.Form):
    username = forms.CharField()

class VolunteerForm(forms.ModelForm):
	class Meta:
		model = VolunteerEvent
		fields = ['username', 'event_name', 'number_hours']

class RemoveVolunteerForm(forms.Form):
	username = forms.CharField()
	event = forms.CharField()
