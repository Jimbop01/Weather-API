import requests
import json


API="3c714514c8a34642bb6124643240110"

aqi="yes"

city_name=input("Enter a city name: ")


forecasturl = f'http://api.weatherapi.com/v1/forecast.json?key={API}&q={city_name}&aqi{aqi}&days=3'




fore_result = requests.get(forecasturl)
fdata = json.loads(fore_result.text)
print(fdata)
print(fdata['location']['name'])
print(fdata['forecast']['forecastday'])