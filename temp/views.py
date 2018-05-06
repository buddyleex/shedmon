from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from django.db.models import Avg, Max
from django.http import JsonResponse
from chartit import DataPool, Chart
from temp.models import *
from temp import settings
from temps.temps import *
from temps.history import *
from temps.livereadout import *
from temps.forecast import *
from temps.mph import *
from temps.pdupower import *

import time
from datetime import timedelta
from datetime import date
from datetime import datetime

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
	history = History(date=date_entry, avgshed=round(avg_choice['shedcur'],2),highshed=round(high_choice['shedcur'],2),avgouts=round(avg_choice['outscur'],2),highouts=round(high_choice['outscur'],2),avggpu=avg_choice['gpuavg'],highgpu=high_choice['gpuhigh'],starttime=previous_day,endtime=current_day)
	history.save()


def history_graph(request,date):
	graph = get_object_or_404(History, date=date)
	graph_data = \
		DataPool(
			series=
			 [{'options': {
			   'source': Entry.objects.filter(time__gte=graph.starttime, time__lt=graph.endtime)},
			  'terms': [
			    ('time', lambda x: x.strftime("%H:%M")),
			    'shedcur',
			    'outscur',
			    'gpuavg']}
			  ])
	graph_display = Chart(
			datasource = graph_data,
			 series_options =
			  [{'options':{
			    'type': 'line',
			    'stacking': False},
			   'terms':{
			     'time': [
				'shedcur',
				'outscur',
				'gpuavg']
			  }}],
			 chart_options =
			   {'title': {
				'text': 'Graph Data'},
			    'xAxis': {
				'title': {
				  'text': date}}})

	return render_to_response('temp/history_graph.html', {'graph_display': graph_display})


def update_entry(request):
	w1_list = filter(settings.W1['FOLDER_REGEX'].search, settings.W1['LIST'])
	gputemps()
	shed_temp()
	outside_temp()
	gpu_choice = gputemps()
	entry = Entry(shedcur=shed_temp(), outscur=outside_temp(),gpuavg=gpu_choice.gpuavg,gpuhigh=gpu_choice.gpuhigh)
	entry.save()

def live_forecast(request):
	 return render(request, 'temp/live_forecast.html', {'forecast' : forecast()[0], 'forecast_alt' : forecast()[1],'forecast_icon' : forecast()[2], 'forecast_am' : forecast()[3], 'forecast_pm' : forecast()[4], 'forecast_date' : forecast()[5]})


def live_power(request):
	pdustats()
	return render(request, 'temp/live_power.html', {'pdupower': pdustats()})


def live_mphpool(request):
	return render(request, 'temp/live_mphpool.html', {'eth_balance' : mph_eth_confirmed_balance(), 'eth_nethash' : mph_eth_dashboard()[0], 'eth_last24hr' : mph_eth_dashboard()[1], 'eth_price' : eth_price(), 'eth_profit': eth_profit()})


def three_day():
	return timezone.now() - timezone.timedelta(days=3)

