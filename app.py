from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder='static')
CORS(app)  # Allow requests from frontend

# Configure Gemini API
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

import requests

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather
    else:
        return None

@app.route("/get-weather", methods=["POST"])
def get_weather_route():
    data = request.get_json()
    destination = data.get("destination", "")

    if not destination:
        return jsonify({"error": "Destination is required!"}), 400

    weather = get_weather(destination)
    if weather:
        return jsonify({"weather": weather})
    else:
        return jsonify({"error": "Could not retrieve weather information."}), 500

@app.route("/generate-itinerary", methods=["POST"])
def generate_itinerary():
    data = request.get_json()
    interest = data.get("interest", "")
    budget = data.get("budget", "")
    destination = data.get("destination", "")
    from_date = data.get("from_date", "")
    to_date = data.get("to_date", "")

    if not all([interest, budget, destination, from_date, to_date]):
        return jsonify({"error": "All fields are required!"}), 400

    # Get weather information
    weather = get_weather(destination)
    weather_info = ""
    if weather:
        weather_info = f"The weather in {destination} is {weather['description']} with a temperature of {weather['temperature']}°C."

    # Generate prompt for Gemini AI
    prompt = f"Create a detailed {interest}-themed travel itinerary for {destination} with a budget of ${budget} from {from_date} to {to_date}. {weather_info} Include daily activities, nearby attractions, food recommendations, and travel tips. Format the itinerary with HTML tags for better readability."

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        itinerary = response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"itinerary": itinerary})

@app.route("/get-nearby-attractions", methods=["POST"])
def get_nearby_attractions():
    data = request.get_json()
    destination = data.get("destination", "")

    if not destination:
        return jsonify({"error": "Destination is required!"}), 400

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(f"List the top tourist attractions in {destination}.")
        attractions = response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"attractions": attractions})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
