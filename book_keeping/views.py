from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm, DeleteEventForm, DonationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def index(request):
    # Home Page for Book Keeping Soft
    return render(request, 'book_keeping/index.html')


def events(request):
    # Show Events
    events = Event.objects.order_by('date_of_event')
    events_dict = {'events': events}
    return render(request, 'book_keeping/events.html', events_dict)


@user_passes_test(lambda u: u.is_superuser)
def new_event(request):
    # Add a new event
    if request.method != 'POST':
        form = EventForm()
    else:
        form = EventForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/new_event.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_event(request):
    if request.method != 'POST':
        form = DeleteEventForm()
    else:
        form = DeleteEventForm(request.POST)
        if form.is_valid:
            data = request.POST.copy()
            name_delete_event = data.get('name')
            Event.objects.filter(name=name_delete_event).delete()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/delete_event.html', context)

@login_required
def donate_event(request):
    #Donate
    if request.method != 'POST':
        form = DonationForm()
    else:
        form = DonationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/donate.html', context)

@login_required
def add_vol(request):
    if request.method != 'POST':
        temp = request.GET['submit']
        # print(temp)
        temp_obj = Event.objects.get(name__startswith=temp)
        # print(temp_obj.num_volunteers)
        # We have enough volunteers, do nothing
        if (temp_obj.num_volunteers_total - temp_obj.num_volunteers) <= 0:
            return redirect('book_keeping:events')
        else:
            temp_obj.num_volunteers += 1
            temp_obj.save()
            return redirect('book_keeping:events')
