# 🌦️ PakWeatherLens Dashboard (Pakistan Weather Insights Dashboard)

**PakWeatherLens** is a real-time weather dashboard that visually presents current and past weather data across popular cities in Pakistan. Built with Python and Streamlit, it combines real-time API data with beautiful visualizations and pixel-art UI elements.


## 🚀 Live Demo

Check out the live dashboard here: https://pakweatherlens-dashboard-kjr8em5ataaebp6qpjsjyt.streamlit.app/

---

## 🚀 Key Features

- 📍 Covers 15+ Pakistani Cities (Karachi, Lahore, Islamabad, etc.)
- ⏳ Compare today's and yesterday's weather
- 🌡️ Visual Metrics:
  - Temperature with pixel-art thermometer icons
  - Humidity with pixel droplet icons
  - Weather conditions with animated pixel visuals
- 📊 Interactive Charts:
  - Temperature trends across cities
  - Humidity heatmaps
  - Radar charts for visual comparison

---

## 🛠️ Technology Stack

### Core Tools
- Python
- Streamlit

### Data Handling
- Pandas

### Visualization
- Matplotlib
- Seaborn

### Weather API Integration
- WeatherAPI
- Requests

### UI & Styling
- CSS
- Pillow (image handling)
- Base64 (for background image embedding)
- Pathlib (file handling)

---

## ⚙️ Installation Guide

### Prerequisites
- Python 3.9+
- Free WeatherAPI key (get from https://www.weatherapi.com/)

### Setup

```bash

 Add your API key
echo "API_KEY=your_weatherapi_key_here" > .env

 Run the app
streamlit run main_app.py


