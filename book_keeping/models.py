from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class VolunteerEvent(models.Model):
    username = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200)
    number_hours = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(8)])


class Event(models.Model):
    """
    This is an event that the admin Creates
    """

    name = models.CharField(max_length=200, unique=True)
    date_of_event = models.DateField(default=date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    num_volunteers_total = models.PositiveIntegerField()
    num_volunteers = models.PositiveIntegerField(default=0)

    def __str__(self):
        """ Return string rep of the Event object """
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


class Donation(models.Model):
    """ This is a donation that is made by a donor """
    username = models.CharField(max_length=50)
    donation = models.DecimalField(max_digits=10, decimal_places=2)
    D_TYPES = (
        ('U', 'Unrestricted'),
        ('R', 'Restricted'),
    )

    donation_type = models.CharField(max_length=1, choices=D_TYPES)
    name_event = models.CharField(max_length=200, blank=True)
