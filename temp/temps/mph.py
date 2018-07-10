import requests
import re
import json
from pysnmp.hlapi import *
import sys
sys.path.append('/home/pi')
from apicalls import mph_api
from minerips import powercost, ethtotalhash, ethpower, dcrtotalhash, dcrpower, btctotalhash, btcpower

requests.packages.urllib3.disable_warnings()


def num_before_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return s.index('.')

def num_of_e(x):
        s = str(x)
        return re.findall(r'[0-9]{2}$',s)


def hash(num):
        if bool(re.search('e',str(num))) == True:
                if int(num_of_e(num)[0]) == int("11"):
                        num = round(float(num/1000000000),2)
                        return str(num) + " Gh/s"
                if int(num_of_e(num)[0]) > int("11") and int(num_of_e(num)[0]) < int("15"):
                        num = round(float(num/1000000000000),2)
                        return str(num) + " Th/s"
                if int(num_of_e(num)[0]) > int("14") and int(num_of_e(num)[0]) < int("18"):
                        num = round(float(num/1000000000000000),2)
                        return str(num) + " Ph/s"
                if int(num_of_e(num)[0]) > int("17") and int(num_of_e(num)[0]) < int("21"):
                        num = round(float(num/1000000000000000000),2)
                        return str(num) + " Eh/s" 

        elif bool(re.search('e',str(num))) == False:
                if num_before_point(num) > int("0") and num_before_point(num) < int("4"):
                        num = round(num,2)
                        return str(num) + " h/s"
                if num_before_point(num) > int("3") and num_before_point(num) < int("7"):
                        num = round(float(num/1000),2)
                        return str(num) + " Kh/s"
                if num_before_point(num) > int("6") and num_before_point(num) < int("10"):
                        num = round(float(num/1000000),2)
                        return str(num) + " Mh/s"
                if num_before_point(num) > int("9") and num_before_point(num) < int("12"):
                        num = round(float(num/1000000000),2)
                        return str(num) + " Gh/s"
        else:
                return "N/A"


def mph_eth_confirmed_balance(): 
        r = requests.get('https://ethereum.miningpoolhub.com/index.php?page=api&action=getuserbalance&api_key=' + mph_api + '&argument=id').json()
        j = r['getuserbalance']['data']['confirmed']
        return j


def mph_eth_dashboard():
        r = requests.get('https://ethereum.miningpoolhub.com/index.php?page=api&action=getdashboarddata&api_key=' + mph_api).json()
        nethash = r['getdashboarddata']['data']['raw']['network']['hashrate']
        last24hr = round(r['getdashboarddata']['data']['recent_credits_24hours']['amount'],4)
        return last24hr


def eth_profit():
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/').json()
        eth_price = round(float(r[0]['price_usd']),2)
	f_eth_price = '${:,.2f}'.format(eth_price)
        r = requests.get('https://whattomine.com/coins/151.json').json()
        block_time = r['block_time']
        block_reward = r['block_reward']
        nethash = r['nethash']
	f_nethash = float(nethash)
	daily_power = ethpower * float(24)
        total_power = ethpower * float(24) * float(30)
        total_cost = total_power * powercost
	daily_cost = daily_power * powercost
        hash_vs_nethash = ethtotalhash / nethash
        block_and_time = float(block_reward) * float(86400) / float(block_time)
        gross_monthly = hash_vs_nethash * block_and_time * eth_price * float(30)
	gross_daily = hash_vs_nethash * block_and_time * eth_price
        unf_net_monthly = round(gross_monthly - total_cost,2)     
        net_monthly = '${:,.2f}'.format(unf_net_monthly)
	unf_net_daily = round(gross_daily - daily_cost,2)
	net_daily = '${:,.2f}'.format(unf_net_daily)
        return net_monthly, net_daily, f_eth_price, unf_net_monthly, unf_net_daily, hash(f_nethash)


def dcr_profit():
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/decred/').json() 
        dcr_price = round(float(r[0]['price_usd']),2) 
	f_dcr_price = '${:,.2f}'.format(dcr_price)
        r = requests.get('https://whattomine.com/coins/152.json').json()
        block_time = r['block_time']
        block_reward = r['block_reward']
        nethash = r['nethash']
	f_nethash = float(nethash)
        daily_power = dcrpower * float(24)
        total_power = dcrpower * float(24) * float(30)
        total_cost = total_power * powercost
        daily_cost = daily_power * powercost
        hash_vs_nethash = dcrtotalhash / nethash
        block_and_time = float(block_reward) * float(86400) / float(block_time)
        gross_monthly = hash_vs_nethash * block_and_time * dcr_price * float(30)
        gross_daily = hash_vs_nethash * block_and_time * dcr_price
        unf_net_monthly = round(gross_monthly - total_cost,2)     
        net_monthly = '${:,.2f}'.format(unf_net_monthly)
        unf_net_daily = round(gross_daily - daily_cost,2)
        net_daily = '${:,.2f}'.format(unf_net_daily)
        return net_monthly, net_daily, f_dcr_price, unf_net_monthly, unf_net_daily, hash(f_nethash)


def btc_profit():
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json() 
        btc_price = round(float(r[0]['price_usd']),2) 
        f_btc_price = '${:,.2f}'.format(btc_price)
        r = requests.get('https://whattomine.com/coins/1.json').json()
        block_time = r['block_time']
        block_reward = r['block_reward']
        nethash = r['nethash']
	f_nethash = float(nethash)
        daily_power = btcpower * float(24)
        total_power = btcpower * float(24) * float(30)
        total_cost = total_power * powercost
        daily_cost = daily_power * powercost
        hash_vs_nethash = btctotalhash / nethash
        block_and_time = float(block_reward) * float(86400) / float(block_time)
        gross_monthly = hash_vs_nethash * block_and_time * btc_price * float(30)
        gross_daily = hash_vs_nethash * block_and_time * btc_price
        unf_net_monthly = round(gross_monthly - total_cost,2)     
        net_monthly = '${:,.2f}'.format(unf_net_monthly)
        unf_net_daily = round(gross_daily - daily_cost,2)
        net_daily = '${:,.2f}'.format(unf_net_daily)
        return net_monthly, net_daily, f_btc_price, unf_net_monthly, unf_net_daily, hash(f_nethash)
