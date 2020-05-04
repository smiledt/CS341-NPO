from django.shortcuts import render, redirect
from .models import Event, Donation, VolunteerEvent
from .forms import EventForm, DeleteEventForm, DonationForm, SummaryForm, VolunteerForm, RemoveVolunteerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

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

@login_required
def volunteer_event(request):
    if request.method != 'POST':
        form = VolunteerForm()
    else:
        form = VolunteerForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            name_event = data.get('event_name')
            username = data.get('username')

            l = VolunteerEvent.objects.filter(username=username)
            e = Event.objects.get(name=name_event)
            can_volunteer = False

            if l.exists():
                for i in l:
                    e2 = Event.objects.get(name=i.event_name)

                    if( (e.start_time != e2.start_time) or (e.end_time != e2.end_time)):
                        can_volunteer = True

            else:
                can_volunteer = True

            if((e.num_volunteers_total - e.num_volunteers - 1 >= 0) and can_volunteer):
                e.num_volunteers = e.num_volunteers + 1
                e.save()
                form.save()

        return redirect('book_keeping:events')

    context = {'form' : form }
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

    context = {'form' : form }
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

    context = {'form' : form }
    return render(request, 'book_keeping/summary_report.html', context)

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
