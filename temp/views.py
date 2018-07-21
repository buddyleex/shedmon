from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from django.db.models import Avg, Max, Count
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
from temps.difficulty import *
from temps.dailyprofit import *
from temps.walletbalance import *
from temps.asicmonitor import *
from temps.gpumonitor import *

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
	return render(request, 'temp/entry_list.html', {'entries': entries})


def history_list(request):
	historys = History.objects.all().order_by('-date')
	return render(request, 'temp/history_list.html', {'historys': historys})


def update_history(request):
	history = History(date=date_entry, avgshed=round(avg_choice['shedcur'],2),highshed=round(high_choice['shedcur'],2),avgouts=round(avg_choice['outscur'],2),highouts=round(high_choice['outscur'],2),avggpu=avg_choice['gpuavg'],highgpu=high_choice['gpuhigh'],starttime=previous_day,endtime=current_day)
	history.save()


def live_gpuminers(request):
	miners = []
	for ip in minerips:
		if claymore_check_rig(ip[0]) is False:
			insert = []
			insert.append(ip[0])
			insert.append("Hash Low")
			insert.append("red")
			miners.append(insert)
		elif claymore_check_rig(ip[0]) == str('offline'):
			insert = []
                        insert.append(ip[0])
                        insert.append("Offline")
			insert.append("red")
                        miners.append(insert)
		elif claymore_check_rig(ip[0]) is True:
			continue
		else:
			continue
	
	if len(miners) == int('0'):
		insert = []
		insert.append("All Miners")
		insert.append("Online")
		insert.append("green")
		miners.append(insert)
		gpuminers = miners
	else:
		gpuminers = miners
					

	return render(request, 'temp/live_gpuminers.html', {'miners': gpuminers})


def live_asicminers(request):
	asicminers = []
	for asic in ants9ips:
		asicminers.append(check_antminer_s9i(asic[0], asic[1], 4028))
	for asic in antd3ips:
		asicminers.append(check_antminer_d3(asic[0], asic[1], 4028))
	for asic in innod9ips:
		asicminers.append(check_inno_d9(asic[0], asic[1], 4028))
	return render(request, 'temp/live_asicminers.html', {'miners' : asicminers})


def live_wallet(request):
	wallet_balance_r = wallet_balance()
	return render(request, 'temp/live_wallet.html', {'total_balance' : wallet_balance_r[0], 'eth_balance' : wallet_balance_r[1], 'eth_balance_price' : wallet_balance_r[2], 
	'btc_balance' : wallet_balance_r[3], 'btc_balance_price' : wallet_balance_r[4], 'aeg_balance' : wallet_balance_r[5], 'aeg_balance_price' : wallet_balance_r[6], 
	'ubiq_balance' : wallet_balance_r[7], 'ubiq_balance_price' : wallet_balance_r[8], 'sia_balance' : wallet_balance_r[9], 'sia_balance_price' : wallet_balance_r[10], 
	'rvn_balance' : wallet_balance_r[11], 'rvn_balance_price' : wallet_balance_r[12], 'xrp_balance' : wallet_balance_r[13], 'xrp_balance_price' : wallet_balance_r[14], 
	'dcr_balance' : wallet_balance_r[15], 'dcr_balance_price' : wallet_balance_r[16]})


def live_mphpool(request):
	eth_profit_r = eth_profit()
	dcr_profit_r = dcr_profit()
	btc_profit_r = btc_profit()
	mph_eth_dashboard_r = mph_eth_dashboard()
	lux_dcr_dashboard_r = lux_dcr_dashboard()
	slush_btc_dashboard_r = slush_btc_dashboard()
        unf_eth_daily = eth_profit_r[4]
        unf_eth_monthly = eth_profit_r[3]
        unf_dcr_daily = dcr_profit_r[4]
        unf_dcr_monthly = dcr_profit_r[3]
        unf_btc_daily = btc_profit_r[4]
        unf_btc_monthly = btc_profit_r[3]
	unf_aeg_price = btc_profit_r[6]
	aeg_profit_r = aeg_profit(unf_aeg_price)
	unf_aeg_daily = aeg_profit_r[4]
	unf_aeg_monthly = aeg_profit_r[3]
        unf_total_daily = unf_eth_daily + unf_dcr_daily + unf_btc_daily + unf_aeg_daily
        total_daily = '${:,.2f}'.format(unf_total_daily)
        unf_total_monthly = unf_eth_monthly + unf_dcr_monthly + unf_btc_monthly + unf_aeg_monthly
        total_monthly = '${:,.2f}'.format(unf_total_monthly)
        return render(request, 'temp/live_mphpool.html', {'eth_balance' : mph_eth_dashboard_r[0], 'eth_hashrate': mph_eth_dashboard_r[1], 'eth_last24hr' : mph_eth_dashboard_r[2], 
	'eth_nethash' : eth_profit_r[5], 'eth_price' : eth_profit_r[2], 'eth_profit' : eth_profit_r[0], 'eth_daily_profit' : eth_profit_r[1], 'dcr_balance': lux_dcr_dashboard_r[0],
	'dcr_hashrate': lux_dcr_dashboard_r[1], 'dcr_nethash' : dcr_profit_r[5], 'dcr_price' : dcr_profit_r[2], 'dcr_profit': dcr_profit_r[0], 'dcr_daily_profit': dcr_profit_r[1], 
	'btc_balance': slush_btc_dashboard_r[0], 'btc_hashrate': slush_btc_dashboard_r[1], 'btc_nethash': btc_profit_r[5], 'btc_price': btc_profit_r[2], 'btc_profit': btc_profit_r[0],
	'btc_daily_profit': btc_profit_r[1], 'aeg_price': aeg_profit_r[2], 'aeg_profit': aeg_profit_r[0], 'aeg_daily_profit': aeg_profit_r[1], 'total_daily': total_daily, 
	'total_monthly': total_monthly, 'eth_coin' : mph_eth_dashboard_r[3]})


def update_difficulty(request):
	for coin in Coins.objects.all():
		updated_diff = update_diff(coin.abv,coin.name,coin.wtm,coin.cmc,coin.polo,coin.grav,coin.cbri,coin.algo)
		update_diffy = Difficulty(abv=updated_diff[0], name=updated_diff[1], price=updated_diff[2], nethash=updated_diff[3], blockr=updated_diff[4], blockt=updated_diff[5], algo=updated_diff[6])
		update_diffy.save()


def display_last_difficulty(request):
	display_last = Difficulty.objects.filter(time__gte=twelve_hours(), time__lt=timezone.now()).order_by('name')	
	return render(request, 'temp/display_last_difficulty.html', {'display_last': display_last})


def display_daily_profit(request):
        return render(request, 'temp/display_daily_profit.html', {'sha256' : sha256(), 'x11' : x11(), 'myrGroestl' : myrGroestl(), 'qubit' : qubit(), 'scrypt' : scrypt(), 'blake14r' : blake14r(),
	'blake2b' : blake2b(), 'daggerHashimoto' : daggerHashimoto(), 'skein' : skein(), 'cNLv1' : cNLv1(), 'cNv7' : cNv7(), 'equihash' : equihash(), 'timeT10' : timeT10(), 'phi1612' : phi1612(), 
	'neoScrypt' : neoScrypt(), 'lyra2REv2' : lyra2REv2(), 'lbry' : lbry(), 'pascal' : pascal(), 'x16R' : x16R(), 'x11Gost' : x11Gost(), 'phi2' : phi2(), 'quark' : quark()})


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
	gpu_choice = gputemps()
	entry = Entry(shedcur=shed_temp(), outscur=outside_temp(),gpuavg=gpu_choice.gpuavg,gpuhigh=gpu_choice.gpuhigh)
	entry.save()


def live_forecast(request):
	update_forecast = forecast()
	return render(request, 'temp/live_forecast.html', {'forecast' : update_forecast[0], 'forecast_alt' : update_forecast[1],'forecast_icon' : update_forecast[2], 'forecast_am' : update_forecast[3], 'forecast_pm' : update_forecast[4], 'forecast_date' : update_forecast[5]})


def live_power(request):
	update_pdupower = pdustats()
	return render(request, 'temp/live_power.html', {'pdupower': update_pdupower})


def live_camera(request):
        return render(request, 'temp/live_camera.html', {})


def three_day():
	return timezone.now() - timezone.timedelta(days=3)


def twelve_hours():
	return timezone.now() - timezone.timedelta(hours=12)
