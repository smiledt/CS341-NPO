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
	num_volunteers_needed = models.IntegerField()
	num_volunteers = models.IntegerField(
		default=0
	)

	def __str__(self):
		# Return string rep of model
		return (self.name + ", " + self.date_of_event + ", " +
				self.start_time + "-" + self.end_time + ", " +
				self.location + ", " +
				self.description + ", " +
				"Volunteers Wanted: " + str(self.num_volunteers_needed - self.num_volunteers))

	# def display(self):
	# 	print('test')
	# 	name = 'test'
	# 	date = self.date_of_event
	# 	return [name, date]
	def test(self):
		self.num_volunteers += 1
		return self
