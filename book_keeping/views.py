from django.shortcuts import render, redirect
from .models import Event, Donation, VolunteerEvent
from .forms import EventForm, DeleteEventForm, DonationForm, SummaryForm, VolunteerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

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


def events(request, error="", message=""):
    """ Show Events """
    events = Event.objects.order_by('date_of_event')
    donor_test = False
    this_user = request.user
    if str(this_user) != 'AnonymousUser':  # Somebody is logged in
        current_donor = this_user.useraccountinfo.is_donor()
        if current_donor:
            donor_test = True

    events_dict = {'events': events, 'message': message,
                   'is_donor': donor_test, 'error_message': error}
    return render(request, 'book_keeping/events.html', events_dict)


def admin_events(request, message=""):
    """ Displays events on the admin page """
    events = Event.objects.order_by('date_of_event')
    events_dict = {'events': events, 'message': message}
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
            return admin_events(request, message="Successfully created event: " + request.POST['name'])

    context = {'form': form}
    return render(request, 'book_keeping/new_event.html', context)


@login_required
def add_vol(request):
    """ Volunteers the user for the event iff there are no conflicts """
    if request.method != 'POST':  # This means the button was clicked on the event page
        event_name = request.GET['volunteer']
        form = VolunteerForm()
        event = Event.objects.get(name=event_name)
        # If we have enough volunteers, do nothing
        if (event.num_volunteers_total - event.num_volunteers) <= 0:
            return events(request, error="We do not need any more volunteers for that event. Thank you!")
        else:  # We do NOT have enough volunteers yet
            context = {'form': form, 'event': event}
            return render(request, 'book_keeping/volunteer_event.html', context)

    else:
        form = VolunteerForm(data=request.POST)
        if form.is_valid():
            # Create a new VolunteerEvent object
            volunteer_event = form.save(commit=False)
            # Grab the event object
            event = Event.objects.get(name=request.POST['volunteer'])
            volunteer_event.event_name = event.name
            volunteer_event.username = request.user.username
            test_volunteer = VolunteerEvent.objects.filter(
                username=volunteer_event.username)
            e2 = Event.objects.get(name=event.name)
            can_volunteer = True

            if test_volunteer.exists():
                for i in test_volunteer:
                    e2 = Event.objects.get(name=i.event_name)
                    if((event.start_time == e2.start_time) or (event.end_time == e2.end_time)):
                        can_volunteer = False

                        if (event.name == e2.name):
                            return events(request, error="You cannot volunteer for the same event twice.")
                        else:
                            return events(request, error="You cannot volunteer for the event: " +
                                          event.name + ". It conflicts with the event you're already volunteering for: " +
                                          e2.name + ".")

            else:
                can_volunteer = True

            if((event.num_volunteers_total - event.num_volunteers - 1 >= 0) and can_volunteer):
                event.num_volunteers = event.num_volunteers + 1
                event.save()
                volunteer_event.save()
                return events(request, message="You have successfully volunteered for " + event.name + ".")

        return redirect('book_keeping:events')

    context = {'form': form}
    return render(request, 'book_keeping/volunteer_event.html', context)

@login_required
def unvolunteer_list(request):
    """ Lists the events the user is currently volunteered for """
    current_user = request.user
    events = VolunteerEvent.objects.filter(username=current_user.username)
    events_dict = {'events': events}
    return render(request, 'book_keeping/unvolunteer_list.html', events_dict)

@login_required
def unvolunteer_event(request):
    """ Unvolunteers the user from the event """
    if request.method == 'POST':
        print("Shouldn't be post!!")  # TODO: Debug code, delete later
    else:
        event_name = request.GET['unvolunteer']
        user = request.user

        volunteer_event = VolunteerEvent.objects.get(username=user.username, event_name=event_name)
        event = Event.objects.get(name=event_name)
        event.num_volunteers -= 1
        volunteer_event.delete()
        event.save()

        return events(request, message="You have successfully unvolunteered for " + event.name + ".")


@user_passes_test(lambda u: u.is_superuser)
def delete_event(request):
    if request.method != 'POST':  # The admin hit the delete event button
        form = DeleteEventForm()
        event_name = request.GET['delete']
        context = {'form': form, 'event_name': event_name}
        return render(request, 'book_keeping/delete_event.html', context)
    else:
        form = DeleteEventForm(request.POST)
        initial_event = Event.objects.get(name=request.POST['delete'])
        if form.is_valid:
            data = request.POST.copy()
            name_delete_event = data.get('name')
            if (name_delete_event != initial_event.name):
                return admin_events(request, message="The event names were not the same. Nothing was deleted.")
            else:
                Event.objects.filter(name=name_delete_event).delete()
                return redirect('book_keeping:admin_events')

    context = {'form': form}
    return render(request, 'book_keeping/delete_event.html', context)


@user_passes_test(lambda u: u.is_superuser)
def summary_report(request):
    # Summary Report
    if request.method == 'POST':
        username_report = request.POST['summary']
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

    users = User.objects.order_by('username')
    context = {'users': users}
    return render(request, 'book_keeping/summary_report.html', context)


@login_required
def donate(request):
    """ Create a donation """
    if request.method != 'POST':  # The user hit the donate button the events page
        form = DonationForm()
        event_name = request.GET['donate']
        context = {'form': form, 'event_name': event_name}

        return render(request, 'book_keeping/donate.html', context)
    else:
        form = DonationForm(data=request.POST)
        if form.is_valid():
            # Create the new donation object
            new_donation = form.save(commit=False)
            # Grab the event object
            event = Event.objects.get(name=request.POST['donate'])
            new_donation.name_event = event.name

            new_donation.username = request.user.username  # Grab the current user
            new_donation.save()
            return events(request, message="Thank you for your donation of $" + str(new_donation.donation) +".")

    context = {'form': form}
    return render(request, 'book_keeping/donate.html', context)
