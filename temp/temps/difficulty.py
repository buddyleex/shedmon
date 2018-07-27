import requests
import re
import json
import sys
requests.packages.urllib3.disable_warnings()

def bitcoin():
	try:
        	r = requests.get('https://poloniex.com/public?command=returnTicker').json()
        	btc_polo = round(float(r['USDT_BTC']['last']),2)
		return btc_polo
	except requests.exceptions.HTTPError:
		return 0
       	except TypeError:
              	price = float('0.0')

def update_diff(abv, name, wtm, cmc, polo, grav, cbri, algo):
	if cmc != int('0'):
		try:
			r1 = requests.get('https://api.coinmarketcap.com/v2/ticker/' + str(cmc) + '/').json()
	        	price = round(float(r1['data']['quotes']['USD']['price']),6)
        		price = '${:,.6f}'.format(price)
		except requests.exceptions.HTTPError:
			price = float('0.0')
		except TypeError:
			price = float('0.0')

	elif polo != '0':
		try:
			r1 = requests.get('https://poloniex.com/public?command=returnTicker').json()
                	btc_price = float(r1[polo]['last'])
			price = round(float(bitcoin()) * float(btc_price),6)
                	price = '${:,.6f}'.format(price)
		except requests.exceptions.HTTPError:
			price = float('0.0')
		except TypeError: 
                        price = float('0.0')

	elif grav != '0':
		try:
        		r1 = requests.get('https://graviex.net//api/v2/tickers.json').json()         
                	btc_price = float(r1[grav]['ticker']['last'])
                	price = round(float(bitcoin()) * float(btc_price),6)
                	price = '${:,.6f}'.format(price)
                except requests.exceptions.HTTPError:
                        price = float('0.0')
                except TypeError: 
                        price = float('0.0')         

        elif cbri != '0':
		try:
                	r1 = requests.get('https://api.crypto-bridge.org/api/v1/ticker')
                	jlo = json.loads(r1.text)    
               		btc_price = float(jlo[int(cbri)]['last'])    
                	price = round(float(bitcoin()) * float(btc_price),6)
                	price = '${:,.6f}'.format(price)
                except requests.exceptions.HTTPError:
                        price = float('0.0')
                except TypeError: 
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
       	else:
               	nethash = '0' 
                blockr = '0' 
                blockt = '0'


	return abv, name, price, nethash, blockr, blockt, algo
