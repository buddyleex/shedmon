import requests
import re
import json
from pysnmp.hlapi import *
import django
import temp.views
from temp.models import *
import sys
sys.path.append('/home/pi')
from apicalls import supr_dcr_api, supr_dcr_id, slush_btc_api, slush_btc_id, mph_api, dcraddress, spaceaddress
from minerips import powercost, ethtotalhash, ethpower, dcrtotalhash, dcrpower, btctotalhash, btcpower, spacepower

requests.packages.urllib3.disable_warnings()

twelve_hours = timezone.now() - timezone.timedelta(hours=12)

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
                        num = round(float(num/1000000000),0)
			num = int(num)
                        return str(num) + " Gh/s"
                if int(num_of_e(num)[0]) > int("11") and int(num_of_e(num)[0]) < int("15"):
                        num = round(float(num/1000000000000),0)
			num = int(num)
                        return str(num) + " Th/s"
                if int(num_of_e(num)[0]) > int("14") and int(num_of_e(num)[0]) < int("18"):
                        num = round(float(num/1000000000000000),0)
			num = int(num)
                        return str(num) + " Ph/s"
                if int(num_of_e(num)[0]) > int("17") and int(num_of_e(num)[0]) < int("21"):
                        num = round(float(num/1000000000000000000),0)
			num = int(num)
                        return str(num) + " Eh/s" 

        elif bool(re.search('e',str(num))) == False:
                if num_before_point(num) > int("0") and num_before_point(num) < int("4"):
                        num = round(num,0)
			num = int(num)
                        return str(num) + " h/s"
                if num_before_point(num) > int("3") and num_before_point(num) < int("7"):
                        num = round(float(num/1000),0)
			num = int(num)
                        return str(num) + " Kh/s"
                if num_before_point(num) > int("6") and num_before_point(num) < int("10"):
                        num = round(float(num/1000000),0)
			num = int(num)
                        return str(num) + " Mh/s"
                if num_before_point(num) > int("9") and num_before_point(num) < int("12"):
                        num = round(float(num/1000000000),0)
			num = int(num)
                        return str(num) + " Gh/s"
        else:
                return "N/A"


def mph_eth_dashboard():
	try:
        	r = requests.get('https://ethereum.miningpoolhub.com/index.php?page=api&action=getuserbalance&api_key=' + mph_api + '&argument=id').json()
        	eth_conf_balance = round(float(r['getuserbalance']['data']['confirmed']),4)
        except requests.exceptions.HTTPError:                
                eth_conf_balance = 'Err'    
        except TypeError:         
                eth_conf_balance = 'Err'    
        except ValueError:        
                eth_conf_balance = 'Err'    
	try:
        	r = requests.get('https://ethereum.miningpoolhub.com/index.php?page=api&action=getdashboarddata&api_key=' + mph_api).json()
        	eth_last24hr = round(r['getdashboarddata']['data']['recent_credits_24hours']['amount'],4)
        except requests.exceptions.HTTPError:                
                eth_last24hr = 'Err'    
        except TypeError:         
                eth_last24hr = 'Err'    
        except ValueError:        
                eth_last24hr = 'Err'    
	try:
        	r = requests.get('https://miningpoolhub.com/index.php?page=api&action=getautoswitchingandprofitsstatistics').json()
        	ethcoin = r['return'][6]['current_mining_coin']
	except requests.exceptions.HTTPError:                
                ethcoin = 'Err'    
        except TypeError:         
                ethcoin = 'Err'    
        except ValueError:        
                ethcoin = 'Err'    
	try:
        	r = requests.get('https://' + ethcoin + '.miningpoolhub.com/index.php?page=api&action=getdashboarddata&api_key=' + mph_api).json()
        	eth_hashrate = round(float(r['getdashboarddata']['data']['raw']['personal']['hashrate'])/float('1000000'),2)
        	eth_hashrate = str(eth_hashrate) + str("Gh/s")
        except requests.exceptions.HTTPError:                
                eth_hashrate = 'Err'
        except TypeError:         
                eth_hashrate = 'Err'
        except ValueError:        
                eth_hashrate = 'Err'
	if ethcoin == "ethereum":
		f_ethcoin = str("ETH")
	elif ethcoin == "ethereum-classic":
		f_ethcoin = str("ETC")
	elif ethcoin == "expanse":
		f_ethcoin = str("EXP")
	elif ethcoin == "musiccoin":
		f_ethcoin = str("MUS")
	else:
		f_ethcoin = str("Err")
        return eth_conf_balance, eth_hashrate, eth_last24hr, f_ethcoin


def supr_dcr_dashboard():
	try:
		r = requests.get('https://dcr.suprnova.cc/index.php?page=api&action=getuserbalance&api_key=' + supr_dcr_api + '&id=' + supr_dcr_id).json()
		dcr_conf_balance = round(float(r['getuserbalance']['data']['confirmed']),4) 
		r = requests.get('https://dcr.suprnova.cc/index.php?page=api&action=getuserworkers&api_key=' + supr_dcr_api + '&id=' + supr_dcr_id).json()
		dcr_hashrate = round(float(r['getuserworkers']['data'][14]['hashrate'])/float('1000000000'),2)
		dcr_hashrate = str(dcr_hashrate) + str("Th/s")
	except requests.exceptions.HTTPError:
      		dcr_conf_balance = 'Err'
		dcr_hashrate = 'Err'
      	except TypeError: 
                dcr_conf_balance = 'Err'    
                dcr_hashrate = 'Err'
       	except ValueError:
                dcr_conf_balance = 'Err'    
                dcr_hashrate = 'Err'
	return dcr_conf_balance, dcr_hashrate


def lux_dcr_dashboard():
	try:
		r = requests.get('http://mining.luxor.tech/API/DCR/user/' + dcraddress).json()
		dcr_conf_balance = float(r['balance'])
		dcr_conf_balance = round(dcr_conf_balance / float('100000000'), 5)
		dcr_hashrate = r['hashrate_1h']
		dcr_hashrate = str(round(float(dcr_hashrate) / float('1000000000000'), 2)) + str('Th/s')
        except requests.exceptions.HTTPError:                
                dcr_conf_balance = 'Err'    
                dcr_hashrate = 'Err'
        except TypeError:         
                dcr_conf_balance = 'Err'    
                dcr_hashrate = 'Err'
        except ValueError:        
                dcr_conf_balance = 'Err'    
                dcr_hashrate = 'Err'
	return dcr_conf_balance, dcr_hashrate


def lux_space_dashboard():
	try:
        	r = requests.get('http://mining.luxor.tech/API/SPACE/user/' + spaceaddress).json()
        	space_conf_balance = float(r['balance'])
		space_conf_balance =  int(round(space_conf_balance / float('1000000000000000000000000'), 0))
        	space_hashrate = r['hashrate_1h']
        	space_hashrate = str(int(round(float(space_hashrate) / float('1000000000'), 0))) + str('Gh/s')
        except requests.exceptions.HTTPError:                
                space_conf_balance = 'Err'    
                space_hashrate = 'Err'
        except TypeError:         
                space_conf_balance = 'Err'    
                space_hashrate = 'Err'
        except ValueError:        
                space_conf_balance = 'Err'    
                space_hashrate = 'Err'
        return space_conf_balance, space_hashrate


def slush_btc_dashboard():
	try:
		r = requests.get('https://slushpool.com/accounts/profile/json/' + slush_btc_api).json()
		btc_conf_balance = round(float(r['confirmed_reward']),5)
		btc_hashrate = round(float(r['hashrate'])/float('1000000'),2)
		btc_hashrate = str(btc_hashrate) + str("Th/s")
		#btc_worker1 = r['workers'][slush_btc_id + '.ants9_1']['alive']
		#btc_worker2 = r['workers'][slush_btc_id + '.ants9_2']['alive']
        except requests.exceptions.HTTPError:                
                btc_conf_balance = 'Err'    
                btc_hashrate = 'Err'
        except TypeError:         
                btc_conf_balance = 'Err'    
                btc_hashrate = 'Err'
        except ValueError:        
                btc_conf_balance = 'Err'    
                btc_hashrate = 'Err'
	return btc_conf_balance, btc_hashrate


def eth_profit():
	coin_name = 'Ethereum'
	find_coin = Coins.objects.filter(name=coin_name)
	for item in find_coin:
		decimal = item.decimal
        find_price = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now(), name=coin_name)
        for item in find_price:
                if item.name == coin_name:
                        unf_coinprice = item.price
			block_time = item.blockt
			block_reward = item.blockr
			nethash = float(item.nethash)
	coin_price = round(unf_coinprice, decimal)
	f_coin_price = '${:,}'.format(coin_price)
	### Edit two Vars below
	daily_power = ethpower * float(24)
        total_power = ethpower * float(24) * float(30)
        total_cost = total_power * powercost
	daily_cost = daily_power * powercost
	### Edit Var below
        hash_vs_nethash = ethtotalhash / nethash 
        block_and_time = float(block_reward) * float(86400) / float(block_time)
        gross_monthly = hash_vs_nethash * block_and_time * coin_price * float(30)
	gross_daily = hash_vs_nethash * block_and_time * coin_price
        unf_net_monthly = round(gross_monthly - total_cost,2)     
        net_monthly = '${:,.2f}'.format(unf_net_monthly)
	unf_net_daily = round(gross_daily - daily_cost,2)
	net_daily = '${:,.2f}'.format(unf_net_daily)
        return net_monthly, net_daily, f_coin_price, unf_net_monthly, unf_net_daily, hash(nethash)


def dcr_profit():
	coin_name = 'Decred'
        find_coin = Coins.objects.filter(name=coin_name)
        for item in find_coin:
                decimal = item.decimal
        find_price = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now(), name=coin_name)
        for item in find_price:
                if item.name == coin_name:
                        unf_coinprice = item.price
                        block_time = item.blockt
                        block_reward = item.blockr
                        nethash = float(item.nethash)
        coin_price = round(unf_coinprice, decimal)    
        f_coin_price = '${:,}'.format(coin_price)
        ### Edit two Vars below
        daily_power = dcrpower * float(24) 
        total_power = dcrpower * float(24) * float(30)    
        total_cost = total_power * powercost
        daily_cost = daily_power * powercost
        ### Edit Var below
        hash_vs_nethash = dcrtotalhash / nethash           
        block_and_time = float(block_reward) * float(86400) / float(block_time)
        gross_monthly = hash_vs_nethash * block_and_time * coin_price * float(30)   
        gross_daily = hash_vs_nethash * block_and_time * coin_price   
        unf_net_monthly = round(gross_monthly - total_cost,2)         
        net_monthly = '${:,.2f}'.format(unf_net_monthly)
        unf_net_daily = round(gross_daily - daily_cost,2)
        net_daily = '${:,.2f}'.format(unf_net_daily)
        return net_monthly, net_daily, f_coin_price, unf_net_monthly, unf_net_daily, hash(nethash) 


def btc_profit():
        coin_name = 'Bitcoin'
        find_coin = Coins.objects.filter(name=coin_name)
        for item in find_coin:
                decimal = item.decimal
        find_price = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now(), name=coin_name)
        for item in find_price:
                if item.name == coin_name:
                        unf_coinprice = item.price
                        block_time = item.blockt
                        block_reward = item.blockr
                        nethash = float(item.nethash)
        coin_price = round(unf_coinprice, decimal)    
        f_coin_price = '${:,}'.format(coin_price)
        ### Edit two Vars below
        daily_power = btcpower * float(24) 
        total_power = btcpower * float(24) * float(30)    
        total_cost = total_power * powercost          
        daily_cost = daily_power * powercost
        ### Edit Var below
        hash_vs_nethash = btctotalhash / nethash           
        block_and_time = float(block_reward) * float(86400) / float(block_time)
        gross_monthly = hash_vs_nethash * block_and_time * coin_price * float(30)   
        gross_daily = hash_vs_nethash * block_and_time * coin_price   
        unf_net_monthly = round(gross_monthly - total_cost,2)         
        net_monthly = '${:,.2f}'.format(unf_net_monthly)
        unf_net_daily = round(gross_daily - daily_cost,2)
        net_daily = '${:,.2f}'.format(unf_net_daily)
        return net_monthly, net_daily, f_coin_price, unf_net_monthly, unf_net_daily, hash(nethash) 


def aeg_profit():
        coin_name = 'Aegeus'
        find_coin = Coins.objects.filter(name=coin_name)
        for item in find_coin:
                decimal = item.decimal
        find_price = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now(), name=coin_name)
        for item in find_price:
                if item.name == coin_name:
                        unf_coinprice = item.price
	coin_price = round(unf_coinprice, decimal)
	f_coin_price = '${:,}'.format(coin_price)
	payoutMN = float('56')
	r = requests.get('http://api-aegeus.mn.zone/masternodes').json()
	totalMN = float(len(r['nodes']))
	dailycycles = float('1440') / float(totalMN)
	partdaily = float('24') * dailycycles
	percdaily = float('24') / partdaily
	parthourly = float('24') * percdaily
	unf_net_daily = (dailycycles * payoutMN * coin_price) - float('0.17')
	net_daily = '${:,.2f}'.format(unf_net_daily)
	monthlycycles = float('720') / parthourly
	unf_net_monthly = (monthlycycles * payoutMN * coin_price) - float('5')
	net_monthly = '${:,.2f}'.format(unf_net_monthly)
	return net_monthly, net_daily, f_coin_price, unf_net_monthly, unf_net_daily 


def space_profit():
	### Edit two Vars below
        daily_power = spacepower * float(24)
        total_power = spacepower * float(24) * float(30)
        total_cost = total_power * powercost
        daily_cost = daily_power * powercost
	unf_net_monthly = round(float('0') - total_cost,2)
	net_monthly = '${:,.2f}'.format(unf_net_monthly)
	unf_net_daily = round(float('0') - daily_cost,2)
	net_daily = '${:,.2f}'.format(unf_net_daily)
	hash = 'N/A'
	f_coin_price = 'N/A'
        return net_monthly, net_daily, f_coin_price, unf_net_monthly, unf_net_daily, hash
