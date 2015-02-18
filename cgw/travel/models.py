from django.db import models
import datetime

class Group(models.Model):
	salt = models.CharField(max_length=50, default='')
	name = models.CharField(max_length=50, default='')

class Person(models.Model):
	name = models.CharField(max_length=50, default='')
	email = models.CharField(max_length=50, default='')
	decided = models.BooleanField(default=False)
	group_id = models.ForeignKey(Group)

class Quote(models.Model):
	dep_date = models.DateTimeField('departure date') #Earliest outgoing flight
	ret_date = models.DateTimeField('return date') #Earliest incoming flight
	direct = models.BooleanField(default=False)
	price = models.FloatField(default=0)
	group_id = models.ForeignKey(Group)
	score = models.IntegerField(default=0)

class Flight(models.Model):
	quote_id = models.ForeignKey(Quote)
	carrier = models.CharField(max_length=30, default='')
	origin = models.CharField(max_length=30, default='')
	destination = models.CharField(max_length=30, default='')
	date = models.DateTimeField('departure date')
	outgoing = models.BooleanField(default=False) #incoming=T,outgoing=F
