import sys
sys.path.append('/home/pi')
from minerips import powercost
from minerspecs import *

## Profit calculator for all algo

def calc_profit(coin,miner):
	daily_power = miner[1] * float(24)
	daily_cost = daily_power * powercost
	hash_vs_nethash = miner[0] / coin.nethash
	block_and_time = float(coin.blockr * float('86400')) / coin.blockt
	#price = coin.price.replace('$','')
	#price = float(price.replace(',',''))
	gross_daily = hash_vs_nethash * block_and_time * coin.price
	unf_net_daily = round(gross_daily - daily_cost,2)
	net_daily = '${:,.2f}'.format(unf_net_daily)
	if unf_net_daily <= float('0'):
		roi = "Inf"
	else:
		roi = int(round(miner[3] / unf_net_daily,0))
	return coin.name, unf_net_daily, net_daily, coin.algo, roi


## Daily profit calculator for single algo

def calc_most_profit(list,miner):
	coinProfit = []
	most_profitable = []
	coinswap = list
	for coin in coinswap:
		coinProfit.append(calc_profit(coin,miner))
	x = 0
	y = len(coinProfit)

	for coin in coinProfit:
		if x == 0:
			most_profitable = coin
			x=x+1
		elif coin[1] > most_profitable[1]:
			x=x+1
			most_profitable = coin
		elif x > y:
			break
		else:
			continue
	
	return most_profitable[0], most_profitable[3], most_profitable[2]
