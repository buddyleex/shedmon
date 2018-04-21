from django.shortcuts import render
from django.utils import timezone
from django.db.models import Avg, Max
from django.http import JsonResponse
from temp.models import *
from temp import settings
from temps.temps import *
from temps.history import *
from temps.livereadout import *
from temps.forecast import *
import time
from datetime import timedelta

# Create your views here.

def home(request):
	return render(request, 'temp/home.html', {})


def live_readout(request):
	return render(request, 'temp/live_readout.html', {'liveshed' : live_shed(), 'liveouts' : live_outside()})


def entry_list(request):
	entries = Entry.objects.filter(time__gte=three_day(), time__lt=timezone.now()).order_by('-time')
	#entries = Entry.objects.all().order_by('-time')
	return render(request, 'temp/entry_list.html', {'entries': entries})


def history_list(request):
	historys = History.objects.all().order_by('-date')
	return render(request, 'temp/history_list.html', {'historys': historys})


def update_history(request):
	current_day = timezone.now()
	previous_day = current_day - timedelta(hours=24)
	date_entry = previous_day.date()

	avg_choice = update_avg(date_entry,previous_day,current_day)
	high_choice = update_high(date_entry,previous_day,current_day)

	history = History(date=date_entry, avgshed=round(avg_choice['shedcur'],2),highshed=round(high_choice['shedcur'],2),avgouts=round(avg_choice['outscur'],2),highouts=round(high_choice['outscur'],2),avggpu=avg_choice['gpuavg'],highgpu=high_choice['gpuhigh'],starttime=previous_day,endtime=current_day)
	history.save()


def update_entry(request):
	w1_list = filter(settings.W1['FOLDER_REGEX'].search, settings.W1['LIST'])
	gputemps()
	gpu_choice = gputemps()
	shed_temp()
	outside_temp()
	entry = Entry(shedcur=shed_temp(), outscur=outside_temp(),gpuavg=gpu_choice.gpuavg,gpuhigh=gpu_choice.gpuhigh)
	entry.save()
	

def live_forecast(request):
	 return render(request, 'temp/live_forecast.html', {'forecast' : forecast()[0], 'forecast_alt' : forecast()[1],'forecast_icon' : forecast()[2], 'forecast_am' : forecast()[3], 'forecast_pm' : forecast()[4], 'forecast_date' : forecast()[5]})


def live_power(request):
	return render(request, 'temp/live_power.html', {})



def three_day():
	return timezone.now() - timezone.timedelta(days=3)
