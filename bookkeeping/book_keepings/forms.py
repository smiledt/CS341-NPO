from django import forms
from .models import Event

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'date_of_event', 'start_time', 'end_time', 'location', 'description', 'num_volunteers']
