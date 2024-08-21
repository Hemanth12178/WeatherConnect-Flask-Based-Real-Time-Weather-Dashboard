from flask import Flask, render_template, request
import requests
import json
import sqlite3

app = Flask(__name__)

# OpenWeather API URL
api_url = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

# Your OpenWeather API key
api_key = "7fabbd23ce3d659083558f73b473307c"

def fetch_weather(city):
    url = api_url.format(city=city, api_key=api_key)
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Convert temperature from Kelvin to Celsius
        temperature_celsius = data["main"]["temp"] - 273.15

        # Convert visibility from meters to kilometers
        visibility_km = data["visibility"] / 1000

        # Construct custom JSON format
        weather_info = {
            "temperature": temperature_celsius,
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "visibility": visibility_km
        }
        print("Weather data fetched successfully:")
        print(json.dumps(weather_info, indent=4))

        return weather_info
    else:
        print("Failed to fetch weather data: ", response.status_code)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    city = request.form['city']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        weather_data = fetch_weather(city)
        if weather_data:
            return render_template('table.html', weather=weather_data)
        else:
            return "Failed to fetch weather data"
    else:
        return 'Login Failed'

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
