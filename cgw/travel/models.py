from django.db import models
import datetime

class Group(models.Model):
	salt = models.CharField(max_length=50, default='')
	name = models.CharField(max_length=50, default='')

class Person(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	decided = models.BooleanField(default=False)
	group_id = models.ForeignKey(Group)

class Quote(models.Model):
	in_carrier = models.CharField(max_length=30)
	out_carrier = models.CharField(max_length=30)
	dep_date = models.DateTimeField('departure date')
	ret_date = models.DateTimeField('return date')
	direct = models.BooleanField(default=False)
	origin = models.CharField(max_length=30)
	destination = models.CharField(max_length=30)
	price = models.IntegerField(default=0)
	#passengers = models.IntegerField(default=0)
	group_id = models.ForeignKey(Group)
	score = models.IntegerField(default=0)	
