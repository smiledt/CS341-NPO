from django.db import models

# Create your models here.
class Event(models.Model):
	# An Event the Admin Creates
	name = models.CharField(max_length=200)
	date_of_event = models.CharField(max_length=10)
	start_time = models.CharField(max_length= 5)
	end_time = models.CharField(max_length =5)
	location = models.CharField(max_length = 200)
	description = models.CharField(max_length= 200)
	num_volunteers = models.IntegerField()

	def __str__(self):
		# Return string rep of model
		return (self.name + " " + self.date_of_event + " " +
				self.start_time + "-" + self.end_time + " " +
				self.location + " " +
				self.description + " " + 
				"Volunteers Wanted: " + str(self.num_volunteers))