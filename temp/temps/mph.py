import requests
import re
import json
import sys
sys.path.append('/home/pi')
from apicalls import mph_api

requests.packages.urllib3.disable_warnings()


#class ChoiceData():
#    def __init__(self, nethash, last24hr):
#        # you can put here some validation logic
#        self.nethash = nethash
#        self.last24hr = last24hr


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
                        return str(num) + " H/s"
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

#def mph_all_balance():
#       r = requests.get('https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key=' + mph_api).json()
#       coins = []
#       key = 0
#       for entry in r['getuserallbalances']['data']:
#               coins.append(r['getuserallbalances']['data'][key]['coin'])
#               coins.append(r['getuserallbalances']['data'][key]['confirmed'])
#               key +=1
#       return coins
        

def mph_eth_dashboard():
        r = requests.get('https://ethereum.miningpoolhub.com/index.php?page=api&action=getdashboarddata&api_key=' + mph_api).json()
        nethash = r['getdashboarddata']['data']['raw']['network']['hashrate']
        last24hr = round(r['getdashboarddata']['data']['recent_credits_24hours']['amount'],4)
        return hash(nethash), last24hr


def eth_price():
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/').json()
        ethprice = round(float(r[0]['price_usd']),2)
        ethprice = "$" + str(ethprice)
        return ethprice

#print mph_eth_confirmed_balance()
#print mph_eth_dashboard()[0]
#print mph_eth_dashboard()[1]
#print eth_price()
