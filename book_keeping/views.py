from django.shortcuts import render, redirect
from .models import Event, Donation, VolunteerEvent
from .forms import EventForm, DeleteEventForm, DonationForm, SummaryForm, VolunteerForm, RemoveVolunteerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from users.models import UserAccountInfo

# Create your views here.

# This will be the index page
# Note: You can only hit this page as an admin user
@user_passes_test(lambda u: u.is_superuser, login_url='/standard_index')
def index(request):
    """ Admin index page """
    return render(request, 'book_keeping/admin_index.html')


# This is the index page for the STANDARD user
def standard_index(request):
    """ Standard user index page """
    return render(request, "book_keeping/index.html")


def events(request):
    """ Show Events """
    events = Event.objects.order_by('date_of_event')
    events_dict = {'events': events, 'is_donor': False}
    this_user = request.user
    if str(this_user) != 'AnonymousUser':  # Somebody is logged in
        current_donor = this_user.useraccountinfo.is_donor()
        if current_donor:
            events_dict = {'events': events, 'is_donor': True}
            print('IT WORKED!')  # TODO: Debug code, delete

    return render(request, 'book_keeping/events.html', events_dict)


def admin_events(request):
    """ Displays events on the admin page """
    events = Event.objects.order_by('date_of_event')
    events_dict = {'events': events}
    return render(request, 'book_keeping/admin_events.html', events_dict)


@user_passes_test(lambda u: u.is_superuser)
def new_event(request):
    """ Add a new event """
    if request.method != 'POST':
        form = EventForm()
    else:
        form = EventForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_keeping:admin_events')

    context = {'form': form}
    return render(request, 'book_keeping/new_event.html', context)


@login_required
def add_vol(request):
    """ Volunteers the user for the event iff there are no conflicts """
    if request.method != 'POST':  # This means the button was clicked on the event page
        event_name = request.GET['volunteer']
        form = VolunteerForm()
        event = Event.objects.get(name=event_name)
        print(event.num_volunteers)  # TODO: Debugging code
        # If we have enough volunteers, do nothing
        if (event.num_volunteers_total - event.num_volunteers) <= 0:
            return redirect('book_keeping:events')
        else:  # We do NOT have enough volunteers yet
            context = {'form': form, 'event': event}
            return render(request, 'book_keeping/volunteer_event.html', context)

    else:  # TODO: Delete or use this code
        form = VolunteerForm(data=request.POST)
        if form.is_valid():
            volunteer_event = form.save(commit=False)  # Create a new VolunteerEvent object
            event = Event.objects.get(name=request.POST['volunteer'])  # Grab the event object
            volunteer_event.event_name = event.name
            print(volunteer_event.event_name)  # Debugging code, delete later
            volunteer_event.username = request.user.username
            print(volunteer_event.username)

            test_volunteer = VolunteerEvent.objects.filter(username=volunteer_event.username)
            e2 = Event.objects.get(name=event.name)
            can_volunteer = True

            if test_volunteer.exists():
                for i in test_volunteer:
                    e2 = Event.objects.get(name=i.event_name)
                    print("Event: {f} Start time: {a} End Time: {b} Start Time {c} End Time: {d} Can volunteer: {e}".format(f=e2.name, a=event.start_time, b=event.end_time, c=e2.start_time, d=e2.end_time, e=can_volunteer))  # TODO: Debugging code, delete this
                    if((event.start_time == e2.start_time) or (event.end_time == e2.end_time)):
                        can_volunteer = False
                        print("Conflict detected")  # TODO: Debugging code, delete later.
                        return redirect('book_keeping:events')

            else:
                can_volunteer = True

            if((event.num_volunteers_total - event.num_volunteers - 1 >= 0) and can_volunteer):
                event.num_volunteers = event.num_volunteers + 1
                event.save()
                volunteer_event.save()

        return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/volunteer_event.html', context)


@login_required
def unvolunteer_event(request):
    if request.method != 'POST':
        form = RemoveVolunteerForm()

    else:
        form = RemoveVolunteerForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            username = data.get('username')
            name = data.get('event')

            l = VolunteerEvent.objects.filter(username=username)

            for i in l:
                if(i.event_name == name):
                    i.delete()

                    e = Event.objects.get(name=name)
                    e.num_volunteers = e.num_volunteers - 1
                    e.save()

        return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/unvolunteer_event.html', context)


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


@user_passes_test(lambda u: u.is_superuser)
def summary_report(request):
    # Summary Report
    if request.method != 'POST':
        form = SummaryForm()
    else:
        form = SummaryForm(request.POST)

        if form.is_valid():
            data = request.POST.copy()
            username_report = data.get('username')
            d = Donation.objects.filter(username=username_report)
            e = VolunteerEvent.objects.filter(username=username_report)

            total = 0
            hours = 0
            for i in d:
                total = total + i.donation

            for j in e:
                hours = hours + j.number_hours

            messages.info(request, 'Donation Total: %.2f' % total)
            messages.info(request, 'Volunteer Hours: %d' % hours)

            return redirect('book_keeping:summary_report')

    context = {'form': form}
    return render(request, 'book_keeping/summary_report.html', context)


@login_required  # TODO: Either use or delete this code
def donate_event(request):
    # Donate
    if request.method != 'POST':
        form = DonationForm()
    else:
        form = DonationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/donate.html', context)


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
        print(temp_event)  # TODO: Debugging code, delete later
        if form.is_valid():
            donation = form.save(commit=False)
            donation.event_name = temp_event
            donation.save()
            return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/donate.html', context)
