import requests
import django
import temp.views
from temp.models import *
import sys
sys.path.append('/home/pi')
from apicalls import ethaddress, dcraddress, dcraddressold, btcaddress, aegaddress, ubiqaddress, siaaddress, rvnaddress, xrpaddress, etherscan_api

requests.packages.urllib3.disable_warnings()

def wallet_balance():
	twelve_hours = timezone.now() - timezone.timedelta(hours=12)
	try:
		r = requests.get('https://api.etherscan.io/api?module=account&action=balance&address=' + ethaddress + '&tag=latest&apikey=' + etherscan_api).json()
		ethbalance = round(float(r['result']) / float('1000000000000000000'),4)
		r = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + etherscan_api).json()
		ethprice = float(r['result']['ethusd'])
		unf_ethbalanceprice = round(ethbalance * ethprice, 2) 
		ethbalanceprice = '${:,.2f}'.format(unf_ethbalanceprice)
        except requests.exceptions.HTTPError:
                ethbalanceprice = 'Err'    
                unf_ethbalanceprice = float('0.0')
        except TypeError:         
                ethbalanceprice = 'Err'    
                unf_ethbalanceprice = float('0.0')
        except ValueError:        
                ethbalanceprice = 'Err'    
                unf_ethbalanceprice = float('0.0')
	try:
		r = requests.get('https://blockchain.info/q/addressbalance/' + btcaddress).json()
		btcbalance = round(float(r) / float('100000000'),5)
		r = requests.get('https://blockchain.info/q/24hrprice').json()
		btcprice = float(r)
		unf_btcbalanceprice = round(btcbalance * btcprice, 2)
		btcbalanceprice = '${:,.2f}'.format(unf_btcbalanceprice)
        except requests.exceptions.HTTPError:                
                btcbalanceprice = 'Err'    
                unf_btcbalanceprice = float('0.0')
        except TypeError:         
                btcbalanceprice = 'Err'    
                unf_btcbalanceprice = float('0.0')
        except ValueError:        
                btcbalanceprice = 'Err'    
                unf_btcbalanceprice = float('0.0')
	try:
        	r = requests.get('https://mainnet.decred.org/api/addr/' + dcraddress + '/balance').json()
        	dcrbalance = round(float(r) / float('100000000'), 2)
		r = requests.get('https://mainnet.decred.org/api/addr/' + dcraddressold + '/balance').json()
		dcrbalanceold = round(float(r) / float('100000000'), 2)
		dcrbalance = dcrbalance + dcrbalanceold
        	r = requests.get('https://api.coingecko.com/api/v3/coins/decred').json()
        	dcrprice = round(float(r['market_data']['current_price']['usd']), 2)
        	unf_dcrbalanceprice = round(dcrbalance * dcrprice, 2)
        	dcrbalanceprice = '${:,.2f}'.format(unf_dcrbalanceprice)
        except requests.exceptions.HTTPError:                
                dcrbalanceprice = 'Err'    
                unf_dcrbalanceprice = float('0.0')
        except TypeError:         
                dcrbalanceprice = 'Err'    
                unf_dcrbalanceprice = float('0.0')
        except ValueError:        
                dcrbalanceprice = 'Err'    
                unf_dcrbalanceprice = float('0.0')
	try:
		r = requests.get('https://chainz.cryptoid.info/aeg/api.dws?q=getbalance&a=' + aegaddress).json()
		aegbalance = round(float(r), 0)
		find_aegprice = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now(), name='Aegeus')
		for item in find_aegprice:
			if item.name == 'Aegeus':
				unf_aegprice = item.price
		aegprice = round(unf_aegprice, 5)
		unf_aegbalanceprice = round(aegbalance * aegprice, 2) 
		aegbalance = int(aegbalance)
		aegbalanceprice = '${:,.2f}'.format(unf_aegbalanceprice)
        except requests.exceptions.HTTPError:                
                aegbalanceprice = 'Err'    
                unf_aegbalanceprice = float('0.0')
        except TypeError:         
                aegbalanceprice = 'Err'    
                unf_aegbalanceprice = float('0.0')
        except ValueError:        
                aegbalanceprice = 'Err'    
                unf_aegbalanceprice = float('0.0')
	try:
		r = requests.get('https://ubiqexplorer.com/api/Balance/' + ubiqaddress).json()
		ubiqbalance = round(float(r), 2)
		r = requests.get('https://ubiqexplorer.com/api/Price').json()
		ubiqprice = round(float(r['priceUsd']), 2)
		unf_ubiqbalanceprice = round(ubiqbalance * ubiqprice, 2)
		ubiqbalanceprice = '${:,.2f}'.format(unf_ubiqbalanceprice)
        except requests.exceptions.HTTPError:                
                ubiqbalanceprice = 'Err'    
                unf_ubiqbalanceprice = float('0.0')
        except TypeError:         
                ubiqbalanceprice = 'Err'    
                unf_ubiqbalanceprice = float('0.0')
        except ValueError:        
                ubiqbalanceprice = 'Err'    
                unf_ubiqbalanceprice = float('0.0')
	try:
		r = requests.get('https://siamining.com/api/v1/addresses/' + siaaddress).json()
		siabalance = round(float(r['paid']), 0)
		r = requests.get('https://siamining.com/api/v1/market').json()
		siaprice = round(float(r['usd_price']), 6)
		unf_siabalanceprice = round(siabalance * siaprice, 2)
		siabalance = int(siabalance)
		siabalanceprice = '${:,.2f}'.format(unf_siabalanceprice)
        except requests.exceptions.HTTPError:                
                siabalanceprice = 'Err'    
                unf_siabalanceprice = float('0.0')
        except TypeError:         
                siabalanceprice = 'Err'    
                unf_siabalanceprice = float('0.0')
        except ValueError:        
                siabalanceprice = 'Err'    
                unf_siabalanceprice = float('0.0')
	try:
		r = requests.get('http://rvnhodl.com/ext/getbalance/' + rvnaddress).json()
		rvnbalance = round(float(r), 0)
		r = requests.get('https://api.coingecko.com/api/v3/coins/ravencoin').json()
		rvnprice = round(float(r['market_data']['current_price']['usd']), 5)
		unf_rvnbalanceprice = round(rvnbalance * rvnprice, 2)
		rvnbalance = int(rvnbalance)
		rvnbalanceprice = '${:,.2f}'.format(unf_rvnbalanceprice)
        except requests.exceptions.HTTPError:                
                rvnbalanceprice = 'Err'    
                unf_rvnbalanceprice = float('0.0')
        except TypeError:         
                rvnbalanceprice = 'Err'    
                unf_rvnbalanceprice = float('0.0')
        except ValueError:        
                rvnbalanceprice = 'Err'    
                unf_rvnbalanceprice = float('0.0')
	try:
		r = requests.get('https://data.ripple.com/v2/accounts/' + xrpaddress).json()
		xrpbalance = round(float(r['account_data']['initial_balance']), 2)
		r = requests.get('https://cex.io/api/tickers/XRP/USD/').json()                
		xrpprice = float(r['data'][5]['last'])       
		unf_xrpbalanceprice = round(xrpbalance * xrpprice, 2)
		xrpbalanceprice = '${:,.2f}'.format(unf_xrpbalanceprice)
        except requests.exceptions.HTTPError:                
                xrpbalanceprice = 'Err'    
                unf_xrpbalanceprice = float('0.0')
        except TypeError:         
                xrpbalanceprice = 'Err'    
                unf_xrpbalanceprice = float('0.0')
        except ValueError:        
                xrpbalanceprice = 'Err'    
                unf_xrpbalanceprice = float('0.0')
	
	unf_total_balance = float('0')
	unf_total_balance = unf_ethbalanceprice + unf_btcbalanceprice + unf_aegbalanceprice + unf_ubiqbalanceprice + unf_siabalanceprice + unf_rvnbalanceprice + unf_xrpbalanceprice + unf_dcrbalanceprice
	total_balance = '${:,.2f}'.format(unf_total_balance)

	return total_balance, ethbalance, ethbalanceprice, btcbalance, btcbalanceprice, aegbalance, aegbalanceprice, ubiqbalance, ubiqbalanceprice, siabalance, siabalanceprice, rvnbalance, rvnbalanceprice, xrpbalance, xrpbalanceprice, dcrbalance, dcrbalanceprice

