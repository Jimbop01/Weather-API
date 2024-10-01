import requests
import json
from flask import Flask

API="574ddfd80439481c9f2122359242709"

aqi="yes"

city_name=input("Enter a city name: ")

url = f"http://api.weatherapi.com/v1/current.json?key={API}&q={city_name}&aqi={aqi}"

result = requests.get(url)

print(result)

wdata = json.loads(result.text)

print(wdata)
name = wdata["location"]["name"]
print(name)