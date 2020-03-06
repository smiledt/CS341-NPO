from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	# Home Page for Book Keeping Soft
	return render(request, 'book_keepings/index.html')

def events(request):
	# Show Events
	events = Event.objects.order_by('date_of_event')
	context = {'events': events}
	return render(request, 'book_keepings/events.html', context)

@login_required
def new_event(request):
	#Add a new event
	if request.method != 'POST':
		form = EventForm()
	else:
		form = EventForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('book_keepings:events')

	context = {'form' : form}
	return render(request, 'book_keepings/new_event.html', context)

@login_required
def add_vol(request):
	if request.method != 'POST':
		temp = request.GET['submit']
		# print(temp)
		temp_obj = Event.objects.get(name__startswith=temp)
		# print(temp_obj.num_volunteers)
		if (temp_obj.num_volunteers_needed - temp_obj.num_volunteers) <= 0: #We have enough volunteers, do nothing
			return redirect('book_keepings:events')
		else:
			temp_obj.num_volunteers += 1
			temp_obj.save()
			return redirect('book_keepings:events')
