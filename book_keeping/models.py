from django.db import models
from datetime import date, time
# Create your models here.
class Donation(models.Model):
    username = models.CharField(max_length=50)
    donation = models.DecimalField(max_digits= 10, decimal_places=2)
    D_TYPES = (
        ('U', 'Unrestricted'),
        ('R', 'Restricted'),
    )

    donation_types = models.CharField(max_length=1, choices=D_TYPES)
    name_event = models.CharField(max_length=200, blank=True)

class VolunteerEvent(models.Model):
    username = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200)
    number_hours = models.IntegerField()

class Event(models.Model):
    """
    This is an event that the admin Creates
    """

    name = models.CharField(max_length=200)
    date_of_event = models.DateField(default=date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    num_volunteers_total = models.IntegerField()
    num_volunteers = models.IntegerField(default=0)

    # def __init__(self, name, date_of_event, start_time, end_time, location, description, num_volunteers_needed):
    #     """ Initialize the event """
    #     self.name = name
    #     self.date_of_event = date_of_event
    #     self.start_time = start_time
    #     self.end_time = end_time
    #     self.location = location
    #     self.description = description
    #     self.num_volunteers = 0
    #     self.num_volunteers_needed = num_volunteers_needed

    def __str__(self):
        """ Return string rep of model"""
        return (self.name + ", " + self.date_of_event + ", "
                + self.start_time + "-" + self.end_time + ", "
                + self.location + ", "
                + self.description + ", "
                + "Volunteers Wanted: " + str(self.num_volunteers_total - self.num_volunteers))

    def get_volunteers_needed(self):
        """ Returns the volunteers still needed"""
        return self.num_volunteers_total - self.num_volunteers

    def has_enough_volunteers(self):
        """ Returns true iff the event has enough volunteers """
        return (self.num_volunteers_total - self.num_volunteers) == 0

    def test(self):
        self.num_volunteers += 1
        return self
