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
                ordering = ['-time']
	time = models.DateTimeField(default=timezone.now)
	shedcur = models.FloatField()
	outscur = models.FloatField()
	gpuavg = models.IntegerField()
	gpuhigh = models.IntegerField()

        def __str__(self):
                return self.time.strftime("%m/%d/%Y, %H:%M:%S")

class History(models.Model):
        class Meta:
                ordering = ['-date']
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

class Coins(models.Model):
	class Meta:
		ordering = ['name']
	abv = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	wtm = models.IntegerField()
	cmc = models.IntegerField()
	polo = models.CharField(max_length=100,default="0")
	grav = models.CharField(max_length=100,default="0")
	cbri = models.CharField(max_length=100,default="0")
	algo = models.CharField(max_length=100,default="none")
	scroll = models.CharField(max_length=3,default="no")
	profit = models.CharField(max_length=3,default="yes")
	decimal = models.IntegerField(default="2")
	

	def __str__(self):
		return self.name

class Difficulty(models.Model):
        class Meta:
                ordering = ['-time']
        time = models.DateTimeField(default=timezone.now)
        abv = models.CharField(max_length=100)
        name = models.CharField(max_length=100)
	price = models.FloatField()
	nethash = models.FloatField()
	blockr = models.FloatField()
	blockt = models.FloatField()
	algo = models.CharField(max_length=100,default="none")

        def __str__(self):
		template = '{0.time} {0.name}'
                return template.format(self)

