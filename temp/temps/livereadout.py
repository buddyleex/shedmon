import os
import glob
import subprocess
import pyowm
import sys
import re
from temp.models import *
import temp.views
import django
import sys
sys.path.append('/home/pi')
from apicalls import pyowm_api, pyowm_city

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


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


def live_shed():
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


def live_outside():
	owm = pyowm.OWM(pyowm_api)
        observation = owm.weather_at_place(pyowm_city)
        w = observation.get_weather()
        s = w.get_temperature('fahrenheit')['temp']
	return s


