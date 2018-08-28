import django
import temp.views
from temp.models import *
import sys
sys.path.append('/home/pi')
from apicalls import cmcapi

def ticker(coins):
	twelve_hours = timezone.now() - timezone.timedelta(hours=12)
	twenty_four_hours = timezone.now() - timezone.timedelta(hours=24)
	diffList_12 = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
	diffList_24 = Difficulty.objects.filter(time__gte=twenty_four_hours, time__lt=timezone.now())
        coinList = []
	coinTicker = []
	coinPrices24 = []
	cmcList = []
	cmcPrices = []
	noncmcPrices = []
	cmcCoinString = ''
	currency = 'USD'
	for coin in coins:
		for item in diffList_24:
			if item.abv == coin[0]:
				#item_price_24 = item.price
                               	#coin_price_24 = float(unf_price_24)
				coin_price_24 = item.price
				appendList = []
				appendList.append(item.abv)
				appendList.append(item.name)
				appendList.append(coin_price_24)
				coinPrices24.append(appendList)
		for item in diffList_12:
			if item.abv == coin[0]:
				if coin[3] > 0:
					cmcList.append(coin)
				if coin[3] == 0:
					#item_price_12 = item.price
					#coin_price_12 = float(unf_price_12)
					coin_price_12 = item.price
					appendList = []
					appendList.append(item.abv)
					appendList.append(item.name)
					appendList.append(item.price)
					noncmcPrices.append(appendList)
	
	for coin in cmcList:
		cmcCoinString = cmcCoinString + coin[0] + ','
	try:
	        rString = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + cmcCoinString[:-1]  + '&convert=' + currency + '&CMC_PRO_API_KEY=' + cmcapi
	        r = requests.get(rString).json()		
	except requests.exceptions.HTTPError:
		coinTicker.append('Error')
		return coinTicker
	except TypeError:
		coinTicker.append('Error')
		return coinTicker
	except ValueError:
		coinTicker.append('Error')
		return coinTicker
	for coin in cmcList:
		appendList = []
                appendList.append(coin[0])
		appendList.append(coin[1])
                appendList.append(round(float(r['data'][coin[0]]['quote'][currency]['price']),coin[2]))
                cmcPrices.append(appendList)
	for coin in cmcPrices:
		for coin24 in coinPrices24:
			if coin24[0] == coin[0]:
				if coin[2] >= coin24[2]:
                                       	direction = 'up'
                                       	color = 'green'
                                else:
                                        direction = 'down'
                                        color = 'red'
				change_1 = float('1') - coin24[2] / float(coin[2])
				change_2 = round(change_1 * float('100'),2)
				change = str(change_2) + '%'
				#price = '${:,}'.format(coin[2])
                               	coinList = []
                               	coinList.append(coin[1])
                              	coinList.append(coin[2])
                               	coinList.append(direction)
                              	coinList.append(color)
                               	coinList.append(change)
				coinTicker.append(coinList)
	for coin in noncmcPrices:
		for coin24 in coinPrices24:
			if coin24[0] == coin[0]:
				if coin[2] >= coin24[2]:
                                        direction = 'up'
                                        color = 'green'
                                else:
                                        direction = 'down'
                                        color = 'red'
                                change_1 = float('1') - coin24[2] / float(coin[2])
                                change_2 = round(change_1 * float('100'),2)
                                change = str(change_2) + '%'
				#price = '${:,}'.format(coin[2])
                                coinList = []
                                coinList.append(coin[1])
                                coinList.append(coin[2])
                                coinList.append(direction)
                                coinList.append(color)
                                coinList.append(change)
                                coinTicker.append(coinList)
				
	return coinTicker
