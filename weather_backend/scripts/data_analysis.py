# data_analysis.py

import sqlite3
import pandas as pd

def fetch_all_data():
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    return df

def analyze_data():
    df = fetch_all_data()
    print("Average Temperature:", df['temperature'].mean())
    print("Max Wind Speed:", df['wind_speed'].max())

# Example usage
if __name__ == "__main__":
    analyze_data()
