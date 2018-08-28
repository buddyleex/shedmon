import requests
import re
import json
import sys
import time
import django
from temp.models import *
import temp.views
requests.packages.urllib3.disable_warnings()

def bitcoin():
	coin_name = 'Bitcoin'
	twelve_hours = timezone.now() - timezone.timedelta(hours=12)
	find_price = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now(), name=coin_name)
        for item in find_price:
                if item.name == coin_name:
                        coin_price = item.price
	return coin_price

def update_diff(abv, name, wtm, cmc, polo, grav, cbri, algo, decimal):
	if cmc != int('0'):
		price = float('0')

	elif polo != '0':
		try:
			r1 = requests.get('https://poloniex.com/public?command=returnTicker').json()
                	btc_price = float(r1[polo]['last'])
			price = round(float(bitcoin()) * float(btc_price),decimal)
		except requests.exceptions.HTTPError:
			price = float('0.0')
		except TypeError: 
                        price = float('0.0')
		except ValueError:
			price = float('0.0')

	elif grav != '0':
		try:
        		r1 = requests.get('https://graviex.net//api/v2/tickers.json').json()         
                	btc_price = float(r1[grav]['ticker']['last'])
                	price = round(float(bitcoin()) * float(btc_price),decimal)
                except requests.exceptions.HTTPError:
                        price = float('0.0')
                except TypeError: 
                        price = float('0.0')         
                except ValueError:
                        price = float('0.0')

        elif cbri != '0':
		try:
                	r1 = requests.get('https://api.crypto-bridge.org/api/v1/ticker')
                	jlo = json.loads(r1.text)    
               		btc_price = float(jlo[int(cbri)]['last'])    
                	price = round(float(bitcoin()) * float(btc_price),decimal)
                except requests.exceptions.HTTPError:
                        price = float('0.0')
                except TypeError: 
                        price = float('0.0') 
                except ValueError:
                        price = float('0.0')

	if wtm != int('0'):                  
		try:                  
                	r2 = requests.get('https://whattomine.com/coins/' + str(wtm) + '.json').json()
                	nethash = float(r2['nethash'])
                	blockr = float(r2['block_reward'])
               		blockt = float(r2['block_time'])
                except requests.exceptions.HTTPError:
                      	nethash = '0' 
                	blockr = '0' 
                	blockt = '0'
                except TypeError: 
                        nethash = '0' 
                        blockr = '0' 
                        blockt = '0'
                except ValueError:
                       	nethash = '0' 
                        blockr = '0' 
                        blockt = '0'
			time.sleep('20')
       	else:
               	nethash = '0' 
                blockr = '0' 
                blockt = '0'


	return abv, name, price, nethash, blockr, blockt, algo
