# cli.py

import sys
from weather_api import get_weather
from database_manager import create_database, insert_weather_data
from data_analysis import analyze_data
from visualization import plot_temperature_trends
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py [command] [arguments]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "setup":
        create_database()
        print("Database created successfully.")
    elif command == "fetch":
        if len(sys.argv) < 3:
            print("Usage: python cli.py fetch [city]")
            sys.exit(1)
        city = sys.argv[2]
        data = get_weather(city)
        if data:
            date = datetime.now().strftime('%Y-%m-%d')
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            insert_weather_data(city, date, temperature, humidity, wind_speed)
            print(f"Weather data for {city} saved.")
        else:
            print("Failed to fetch weather data.")
    elif command == "analyze":
        analyze_data()
    elif command == "plot":
        plot_temperature_trends()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
