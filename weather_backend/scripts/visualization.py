# visualization.py

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

def plot_temperature_trends():
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    
    plt.plot(df['date'], df['temperature'], marker='o')
    plt.title('Temperature Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    plot_temperature_trends()
