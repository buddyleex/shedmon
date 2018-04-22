import temp.views
import django
import requests
import re

api_address='http://api.openweathermap.org/data/2.5/forecast?appid=2cc6c9fc14c80bb92a8d50c35eaca912&q='
city = 'keller,us'
url = api_address + city
json_data = requests.get(url).json()

def forecast():
        f_date = json_data['list'][0]['dt_txt']
        re_date = re.search('[0-9]+:[0-9]+:[0-9]+$',f_date).group(0)
        
        if re_date == "00:00:00":
                x = 4
                y = 7
        if re_date == "03:00:00":         
                x = 3        
                y = 6        
        if re_date == "06:00:00":                
                x = 2                
                y = 5                
        if re_date == "09:00:00":                        
                x = 1                        
                y = 4                         
        if re_date == "12:00:00":                                
                x = 8                                
                y = 3                                
        if re_date == "15:00:00":                                        
                x = 7                                        
                y = 2                                        
        if re_date == "18:00:00":                                                
                x = 6                                                
                y = 1                                                
        if re_date == "21:00:00":                                                        
                x = 5                                                        
                y = 8
        
        f_fore = json_data['list'][y]['weather'][0]['main']
        f_desc = json_data['list'][y]['weather'][0]['description'] 
        f_icon = json_data['list'][y]['weather'][0]['icon']
        f_tempam = json_data['list'][x]['main']['temp'] 
        f_temppm = json_data['list'][y]['main']['temp'] 
        f_dt = json_data['list'][y]['dt_txt'] 


        f_tempam = round(f_tempam * 9.0 / 5.0 - 459.67, 2)
        f_temppm = round(f_temppm * 9.0 / 5.0 - 459.67, 2)
        f_dt_month = re.search('-[0-9]{2}-',f_dt).group()
        f_dt_month = f_dt_month.replace("-","",2)
        f_dt_day = re.search('-[0-9]{2}\s',f_dt).group()
        f_dt_day = f_dt_day.replace("-","",1)
        f_dt_day = f_dt_day.replace(" ","",1)
        f_dt_year = re.search('^[0-9]{4}',f_dt).group()
        f_date = f_dt_month + "/" + f_dt_day + "/" + f_dt_year
        

        return f_fore, f_desc, f_icon, f_tempam, f_temppm, f_date

