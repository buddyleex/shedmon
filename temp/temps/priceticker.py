import django
import temp.views
from temp.models import *


def ticker():
	twelve_hours = timezone.now() - timezone.timedelta(hours=12)
	twenty_four_hours = timezone.now() - timezone.timedelta(hours=24)
	coins = ['Bitcoin','Ethereum','Litecoin','Decred','Sia','Ravencoin','Aegeus','Ethereum Classic','Expanse','Ubiq','LBRY Credits','Ripple','Luxcoin','Zcash']
	diffList_12 = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
	diffList_24 = Difficulty.objects.filter(time__gte=twenty_four_hours, time__lt=timezone.now())
        coinList = []
	coinTicker = []
	for coin in coins:
		for item in diffList_24:
			if item.name == coin:
				item_price_24 = item.price
                               	unf_price = item_price_24.replace('$','')
				unf_price_24 = unf_price.replace(',','')
                               	coin_price_24 = float(unf_price_24)

		for item in diffList_12:
			if item.name == coin:
				if coin == 'Bitcoin' or coin == 'Ethereum' or coin == 'Decred' or coin == 'Sia':
					coinModel = Coins.objects.filter(name=coin).get()
					cmc = coinModel.cmc
					try:
                        			r = requests.get('https://api.coinmarketcap.com/v2/ticker/' + str(cmc) + '/').json()
                        			coin_price_12 = round(float(r['data']['quotes']['USD']['price']),6)
                			except requests.exceptions.HTTPError:
                        			coin_price_12 = float('0')
                			except TypeError:
                        			coin_price_12 = float('0')
					if coin == 'Sia' or coin == 'Ravencoin' or coin == 'Aegeus':
                                     		price = '${:,.5f}'.format(coin_price_12)
					else:
						price = '${:,.2f}'.format(coin_price_12)
					if coin_price_12 >= coin_price_24:
						direction = 'up'
						color = 'green'
					else:
						direction = 'down'
						color = 'red'
					change_1 = float('1') - float(coin_price_24 / coin_price_12)
					change_2 = round(change_1 * float('100'),2)
					change = str(change_2) + '%'

                                        coinList = []
                                        coinList.append(coin)
                                        coinList.append(price)
                                        coinList.append(direction)
                                        coinList.append(color)
                                        coinList.append(change)

				else:
					item_price_12 = item.price
					unf_price = item_price_12.replace('$','')
					unf_price_12 = unf_price.replace(',','')
					coin_price_12 = float(unf_price_12)
					if item.name == 'Sia' or item.name == 'Ravencoin' or item.name == 'Aegeus':
						price = '${:,.5f}'.format(coin_price_12)
					else:
						price = '${:,.2f}'.format(coin_price_12)
					if coin_price_12 >= coin_price_24:
						direction = 'up'
						color = 'green'
					else:
						direction = 'down'
						color = 'red'
					change_1 = float('1') - float(coin_price_24 / coin_price_12)
					change_2 = round(change_1 * float('100'),2)
					change = str(change_2) + '%'

        				coinList = []
					coinList.append(coin)
					coinList.append(price)
					coinList.append(direction)
					coinList.append(color)
					coinList.append(change)

				coinTicker.append(coinList)
	return coinTicker
