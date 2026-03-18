from flask import Flask, render_template
import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/api/debug")
def debug():
    return {
        "api_key_present": bool(os.getenv("API_KEY")),
        "lat": os.getenv("LAT", "12.97"),
        "lon": os.getenv("LON", "77.59")
    }

def get_sensor_data():
    api_key = os.getenv("API_KEY")
    lat = os.getenv("LAT", "12.97")
    lon = os.getenv("LON", "77.59")

    if not api_key:
        return {"error": "API_KEY not set"}

    weather_url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={api_key}"

    try:
        # 🌦 WEATHER DATA
        weather_res = requests.get(weather_url, timeout=5)
        weather_res.raise_for_status()
        weather_json = weather_res.json()

        weather_data = weather_json["data"][0]

        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": weather_data.get("city_name"),

            # 🌡 Temperature
            "temperature": weather_data.get("temp"),
            "feels_like": weather_data.get("app_temp"),
            "dew_point": weather_data.get("dewpt"),

            # 💧 Humidity
            "humidity": weather_data.get("rh"),

            # 🌬 Pressure & Wind
            "pressure": weather_data.get("pres"),
            "wind_speed": weather_data.get("wind_spd"),
            "wind_direction": weather_data.get("wind_cdir_full"),

            # ☁ Clouds & Conditions
            "clouds": weather_data.get("clouds"),
            "weather": weather_data.get("weather", {}).get("description"),

            # 🌧 Rain / Snow
            "precipitation": weather_data.get("precip"),
            "snowfall": weather_data.get("snow"),

            # 👁 Visibility
            "visibility": weather_data.get("vis"),

            # ☀ Solar & UV
            "solar_radiation": weather_data.get("solar_rad"),
            "uv_index": weather_data.get("uv"),
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route("/")
def dashboard():
    data = get_sensor_data()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

print("API KEY:", api_key)

