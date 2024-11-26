from datetime import datetime
import json
import requests
from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_admin import Admin, form
from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt
#from werkzeug.security import generate_password_hash, check_password_hash
admin = Admin()
app=Flask(__name__)
app.secret_key='secret'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/739329/OneDrive - New College Swindon/Weather API/database.db'

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


bcrypt=Bcrypt(app)
db = SQLAlchemy(app)
admin.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def weatherapi():
    if request.method=='POST':
        cityname=request.form.get('cityname')
        if cityname == "":
            return render_template("home.html", placeholder='Enter a city name',logged_in=logged_in)

        return redirect(f'/output/{cityname}')
    return render_template('home.html', placeholder='London...')

@app.route('/output/<cityname>')
def output(cityname):
    try:
        API = "3c714514c8a34642bb6124643240110"

        aqi = "yes"

        #url = f'http://api.weatherapi.com/v1/current.json?key={API}&q={cityname}&aqi={aqi}'
        #result = requests.get(url)
        #wdata = json.loads(result.text)

        forecasturl = f'http://api.weatherapi.com/v1/forecast.json?key={API}&q={cityname}&aqi{aqi}&days=7'
        result=requests.get(forecasturl)
        fdata = json.loads(result.text)
        #print(fdata)

        city_name =(fdata['location']['name'])
        region = (fdata['location']['region']+", "+fdata['location']['country'])
        temp_c = fdata['current']['temp_c']
        feelslike_c = fdata['current']['feelslike_c']
        condition_txt=fdata['current']['condition']['text']
        condition_img=fdata['current']['condition']['icon']
        wind_mph = fdata['current']['wind_mph']
        wind_dir = fdata['current']['wind_dir']
        precip_mm= fdata['current']['precip_mm']
        humidity = fdata['current']['humidity']
        #air_qual = fdata['current']['air_quality']

        forecast = fdata['forecast']['forecastday']

        day1 = (datetime.strptime(forecast[0]["date"],'%Y-%m-%d').date()).strftime('%d/%m/%y')
        day2 = (datetime.strptime(forecast[1]["date"], '%Y-%m-%d').date()).strftime('%d/%m/%y')
        day3 = (datetime.strptime(forecast[2]['date'], '%Y-%m-%d').date()).strftime('%d/%m/%y')


        return render_template('output.html', cityname=cityname.capitalize(),
                               city_name=city_name, region=region,temp_c=temp_c, feelslike_c=feelslike_c,
                               wind_mph=wind_mph,wind_dir=wind_dir, condition_img=condition_img,
                               condition_txt=condition_txt, precip_mm=precip_mm, humidity=humidity,
                               forecast=forecast,day1=day1,day2=day2,day3=day3)
    except:
        return render_template('home.html',template='enter a valid city') and redirect('/')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        query = Users.query.filter_by(username=username).first()
        if query is not None:
            flash(f'username already exists')
            return render_template('register.html')
        else:
            if password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                u = Users(username = username, password = hashed_password)
                db.session.add(u)
                db.session.commit()
                flash(f'account successfully created')
                return redirect('/login')
    return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        is_valid = bcrypt.check_password_hash(user.password,password)
        print(is_valid)
        if is_valid:
            flash(f'welcome to the weather API {username}')
            session['username'] = username
            login_user(user)
            #logged_in=True
            return  redirect('/')
        else:
            flash(f'incorrect username or password')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/profile')
def profile():
    username = session['username']
    return render_template('profile.html',username=username)
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

admin.add_view(ModelView(Users,db.session))

global logged_in
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)