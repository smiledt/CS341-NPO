from django.db import models
from datetime import date
from django import forms
# Create your models here.


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

    def __str__(self):
        """ Return string rep of model"""
        return (self.name + ", " + str(self.date_of_event) + ", "
                + str(self.start_time) + "-" + str(self.end_time) + ", "
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


class Donation(models.Model):
    """ This is a Donation that is made by a donor """
    donation = models.DecimalField(max_digits=10, decimal_places=2)
    D_TYPES = (('U', 'Unrestricted'), ('R', 'Restricted'),)
    donation_type = models.CharField(max_length=1, choices=D_TYPES)
    event_name = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=True)
