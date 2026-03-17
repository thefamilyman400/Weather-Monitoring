# app.py
from flask import Flask, render_template
import random, datetime
import requests

app = Flask(__name__)

def get_sensor_data():
    api_key = "251937a14278489cbd9d97e628adcc9f"  # replace with your Weatherbit key
    lat, lon = 12.97, 77.59   # Bengaluru coordinates
    url = f"https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={api_key}"

    response = requests.get(url).json()
    data = response["data"][0]

    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data["temp"],         # °C
        "humidity": data["rh"],              # %
        "soil_moisture": data.get("soil_moisture", "N/A")  # may depend on plan
    }
@app.route("/")
def dashboard():
    data = get_sensor_data()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)