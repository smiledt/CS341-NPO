from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm, DonationForm
from django.contrib.auth.decorators import login_required
from users.models import UserAccountInfo
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    """ Home Page for Book Keeping app, which is the event page """
    return render(request, 'book_keeping/index.html')


def events(request):
    """ Show Events """
    events = Event.objects.order_by('date_of_event')
    events_dict = {'events': events, 'is_donor': False}
    this_user = request.user
    if str(this_user) != 'AnonymousUser':  # Somebody is logged in
        current_donor = this_user.useraccountinfo.is_donor()
        if current_donor:
            events_dict = {'events': events, 'is_donor': True}
            print('IT WORKED!')

    return render(request, 'book_keeping/events.html', events_dict)


@login_required
def new_event(request):
    """ Add a new event """
    if request.method != 'POST':
        form = EventForm()
    else:
        form = EventForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/new_event.html', context)


@login_required
def add_vol(request):
    """ Add a volunteer to an event """
    # This method needs to be tweaked and changed by Derek
    if request.method != 'POST':
        temp = request.GET['volunteer']
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


@login_required
def donate(request):
    """ Create a donation """
    if request.method != 'POST':
        form = DonationForm()
        event_name = request.GET['donate']
        context = {'form': form, 'event_name': event_name}

        return render(request, 'book_keeping/donate.html', context)
    else:
        temp_event = Event.objects.get(name__startswith=request.POST['donate'])
        form = DonationForm(data=request.POST)
        form.event_name = temp_event  # Do we need this?
        # form.fields.update([('event_name', temp_event)])
        # form = DonationForm(data=request.POST, initial={'event_name': temp_event})
        print(temp_event)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.event_name = temp_event
            donation.save()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/donate.html', context)
