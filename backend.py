# app.py
from flask import Flask, render_template
import random, datetime

app = Flask(__name__)

def get_sensor_data():
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(random.uniform(18, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "soil_moisture": round(random.uniform(20, 80), 2)
    }

@app.route("/")
def dashboard():
    data = get_sensor_data()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)