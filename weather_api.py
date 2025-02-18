# weather_api.py

import requests
import json

API_KEY = '42d5f1c20887b5de75e7d423664871b8'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    url = f'{BASE_URL}?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API call failed with status {response.status_code}: {response.text}"}

# Example usage
if __name__ == "__main__":
    city = input("Enter city name: ")
    data = get_weather(city)
    if data:
        print(json.dumps(data, indent=4))
    else:
        print("Failed to retrieve data")
