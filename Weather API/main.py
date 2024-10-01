import requests
import json
from flask import Flask, render_template, request, redirect
import sqlite3

app=Flask(__name__)
app.secret_key='secret'



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def weatherapi():
    if request.method=='POST':
        cityname=request.form.get('cityname')
        if cityname == "":
            return render_template("home.html", placeholder='Enter a city name')

        return redirect(f'/output/{cityname}')
    return render_template('home.html', placeholder='London...')

@app.route('/output/<cityname>')
def output(cityname):
    try:
        API = ""

        aqi = "yes"

        url = f'http://api.weatherapi.com/v1/current.json?key={API}&q={cityname}&aqi={aqi}'
        result = requests.get(url)
        wdata = json.loads(result.text)

        city_name =(wdata['location']['name'])
        region = (wdata['location']['region']+", "+wdata['location']['country'])
        temp_c = wdata['current']['temp_c']
        feelslike_c = wdata['current']['feelslike_c']
        condition_txt=wdata['current']['condition']['text']
        condition_img=wdata['current']['condition']['icon']
        wind_mph = wdata['current']['wind_mph']
        wind_dir = wdata['current']['wind_dir']
        precip_mm= wdata['current']['precip_mm']
        humidity = wdata['current']['humidity']

        return render_template('output.html', cityname=cityname.capitalize(),
                               city_name=city_name, region=region,temp_c=temp_c, feelslike_c=feelslike_c,
                               wind_mph=wind_mph,wind_dir=wind_dir, condition_img=condition_img,condition_txt=condition_txt, precip_mm=precip_mm, humidity=humidity)
    except:
        return render_template('home.html',template='enter a valid city') and redirect('/')




if __name__ == '__main__':
    app.run(debug=True)
