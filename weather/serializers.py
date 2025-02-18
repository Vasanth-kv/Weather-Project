from datetime import datetime
from rest_framework import serializers

from weather_api import get_weather
from .models import Weather

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['city', 'date', 'temperature', 'humidity', 'wind_speed']

    def validate_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value
    def create(self, validated_data):
        city = validated_data['city']
        date = validated_data['date']
        
        # Fetch weather data from the API
        weather_data = get_weather(city)
        if weather_data:
            validated_data['temperature'] = weather_data['main']['temp']
            validated_data['humidity'] = weather_data['main']['humidity']
            validated_data['wind_speed'] = weather_data['wind']['speed']
        else:
            raise serializers.ValidationError("Unable to fetch weather data for the specified city.")
        
        return super().create(validated_data)

    # def validate_temperature(self, value):
    #     if not (-100 <= value <= 60):
    #         raise serializers.ValidationError("Temperature must be between -100 and 60 degrees Celsius.")
    #     return value

    # def validate_humidity(self, value):
    #     if not (0 <= value <= 100):
    #         raise serializers.ValidationError("Humidity must be between 0 and 100 percent.")
    #     return value

    # def validate_wind_speed(self, value):
    #     if not (0 <= value <= 150):
    #         raise serializers.ValidationError("Wind speed must be between 0 and 150 m/s.")
    #     return value
