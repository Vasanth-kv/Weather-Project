# database_manager.py

import sqlite3

def create_database():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather
                 (city TEXT, date TEXT, temperature REAL, humidity REAL, wind_speed REAL)''')
    conn.commit()
    conn.close()

def insert_weather_data(city, date, temperature, humidity, wind_speed):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?)",
              (city, date, temperature, humidity, wind_speed))
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    create_database()
    insert_weather_data('London', '2024-08-30', 20.5, 65, 5.2)
