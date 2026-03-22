# 🌤 Weather DevOps App

A production-ready weather dashboard built with Flask, Docker, and Nginx.

## 🚀 Features
- Real-time weather data (OpenWeather API)
- Autocomplete city search
- 5-day forecast chart
- Clean UI dashboard

## 🧱 Tech Stack
- Python (Flask)
- Docker & Docker Compose
- Nginx (Reverse Proxy)
- Chart.js

## 🏗 Architecture
User → Nginx → Flask (Gunicorn)

## ▶️ Run Locally

```bash
docker-compose up --build -d