from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def format_weather(data):
    tz = pytz.FixedOffset(data["timezone"] // 60)

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "desc": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
        "time": datetime.now(tz).strftime("%d-%m-%Y %H:%M")
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q")

    if not query:
        return jsonify([])

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}"
    data = requests.get(url).json()

    cities = []
    for item in data:
        name = item["name"]
        state = item.get("state")
        country = item["country"]

        if state:
            cities.append(f"{name}, {state}, {country}")
        else:
            cities.append(f"{name}, {country}")

    return jsonify(cities)


@app.route("/weather_by_city")
def weather_by_city():
    city = request.args.get("city")

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        return jsonify(format_weather(data))

    return jsonify({"error": "City not found"}), 404


@app.route("/weather_by_coords")
def weather_by_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        return jsonify(format_weather(data))

    return jsonify({"error": "Failed"}), 400


@app.route("/forecast")
def forecast():
    city = request.args.get("city")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    if "list" not in data:
        return jsonify({"temps": [], "times": []})

    temps = []
    times = []

    for i in range(0, len(data["list"]), 8):
        entry = data["list"][i]
        temps.append(entry["main"]["temp"])
        times.append(entry["dt_txt"])

    return jsonify({"temps": temps, "times": times})


if __name__ == "__main__":
    app.run(debug=True)