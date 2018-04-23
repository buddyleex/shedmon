import os
import glob
import time
import datetime
import subprocess
import pyowm
import sys
import re
import requests
import json
from temp.models import *
import temp.views
import django
from django.http import request
import sys
sys.path.append('/home/pi')
from apicalls import pyowm_api, pyowm_city

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
requests.packages.urllib3.disable_warnings()

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
script_dir = os.path.dirname(os.path.abspath(__file__))
print os.path.join(script_dir, '../temp/')
sys.path.append(os.path.join(script_dir, '../temp/'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "temp.settings")
w1_list = glob.glob("/sys/bus/w1/devices/*")
w1_folder_regex = re.compile('\d+-\d+')
sensor_reading_regex = re.compile('[\d]+\n')
w1_list = filter(w1_folder_regex.search, w1_list)


def shed_temp():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                temp_z = round(temp_f, 2)
	return temp_z


def outside_temp():
	owm = pyowm.OWM(pyowm_api)
        observation = owm.weather_at_place(pyowm_city)
        w = observation.get_weather()
        s = w.get_temperature('fahrenheit')['temp']
	return s


class ChoiceData():
    def __init__(self, gpuavg, gpuhigh):
        # you can put here some validation logic
        self.gpuavg = gpuavg
        self.gpuhigh = gpuhigh

def gputemps():
        temptot = list()
        with open('/home/pi/minerips.txt') as fi:
                for line in fi:
                        try:
                                r = requests.get('http://' + str.strip(line) + ':3333')
                                d = {"id":"0","jsonrpc":"2.0","method":"miner_getstat1"}
                                t = re.search('\{[^\}]+\}', r.text)
                                j = json.loads(t.group(0))
                                dict = j['result']

                                temps = dict[6]
                                tempz = [[]]


                                i = 6
                                y = 0

                                firstcard = int(temps[0] + temps[1])
                                tempz.append(firstcard)

                                while i < len(temps):
                                        y = y + 1
                                        z = i + 1
                                        tempentry = int(temps[i] + temps[z])
                                        tempz.append(tempentry)
                                        temptot.append(tempz[y])
                                        i = i + 6
        
                                if i > len(temps):
                                        y = y + 1
                                        tempz.append(tempentry)
                                        temptot.append(tempz[y])

                                if 'str' in line:
                                        break
        

                        except requests.exceptions.ConnectionError:
                                continue                

                
                sum = 0
                ct = 0

                for element in temptot:
                        sum+=element
                        ct=ct+1


                gpuavg = sum/ct
                gpuhigh = max(temptot)
				
        return ChoiceData(gpuavg, gpuhigh)


gpu_choice = gputemps()

entry = Entry(shedcur=shed_temp(), outscur=outside_temp(),gpuavg=gpu_choice.gpuavg,gpuhigh=gpu_choice.gpuhigh)
entry.save()
