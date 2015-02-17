from django.db import models
import datetime

class Quote(models.Model):
	inCarrier = models.CharField(max_length=30)
	outCarrier = models.CharField(max_length=30)
	depDate = models.DateTimeField('departure date')
	retDate = models.DateTimeField('return date')
	direct = models.BooleanField(default=False)
	origin = models.CharField(max_length=30)
	destination = models.CharField(max_length=30)
	price = models.IntegerField(default=0)
