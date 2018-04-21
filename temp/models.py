from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import os
import glob
import datetime
import subprocess
import pyowm
import requests
import re



# Create your models here.


class Entry(models.Model):
        class Meta:
                ordering = ['time']
	time = models.DateTimeField(default=timezone.now)
	shedcur = models.FloatField()
	outscur = models.FloatField()
	gpuavg = models.IntegerField()
	gpuhigh = models.IntegerField()

        def __str__(self):
                return self.time.strftime("%m/%d/%Y, %H:%M:%S")

class History(models.Model):
        class Meta:
                ordering = ['date']
	date = models.DateField()
	avgshed = models.FloatField()
	highshed = models.FloatField()
        avgouts = models.FloatField()
	highouts = models.FloatField()
        avggpu = models.IntegerField()
        highgpu = models.IntegerField()	
	starttime = models.DateTimeField()
        endtime = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.date.strftime("%m/%d/%Y")
