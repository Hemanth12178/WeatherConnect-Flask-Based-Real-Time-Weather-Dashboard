import requests
import json
import time
import paho.mqtt.client as mqtt

# OpenWeather API URL
api_url = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

# Your OpenWeather API key
api_key = "7fabbd23ce3d659083558f73b473307c"

# City for which you want to fetch weather data
city ="coimbatore"

# MQTT Broker
mqtt_broker = "f3c001edf9714f96bc027d0eee58efda.s1.eu.hivemq.cloud"  # Replace with your MQTT broker address
mqtt_port = 8883
mqtt_topic = "weather"
mqtt_username = "hivemq.webclient.1709295132519"
mqtt_password = "0kYn?7sgQ5&#q1Dc$JTC"


def fetch_weather():
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
        print(json.dumps(weather_info, indent=4))  # Print custom JSON format
        return weather_info
    else:
        print("Failed to fetch weather data: ", response.status_code)
        return None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid, qos=None, properties=None):
    print("Message published")



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)

while True:
    weather_data = fetch_weather()
    if weather_data:
        client.publish(mqtt_topic, json.dumps(weather_data))
        print("Connected to MQTT Broker")
        print("Weather data published to MQTT broker")
    else:
        print("Failed to publish weather data")
    time.sleep(5) #secs
