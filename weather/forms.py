from datetime import datetime
from django import forms
from .models import Weather

class WeatherForm(forms.ModelForm):
    class Meta:
        model = Weather
        fields = ['city', 'date', 'temperature', 'humidity', 'wind_speed']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > datetime.now().date():
            raise forms.ValidationError("The date cannot be in the future.")
        return date

    # def clean_temperature(self):
    #     temperature = self.cleaned_data.get('temperature')
    #     if not (-100 <= temperature <= 60):
    #         raise forms.ValidationError("Temperature must be between -100 and 60 degrees Celsius.")
    #     return temperature

    # def clean_humidity(self):
    #     humidity = self.cleaned_data.get('humidity')
    #     if not (0 <= humidity <= 100):
    #         raise forms.ValidationError("Humidity must be between 0 and 100 percent.")
    #     return humidity

    # def clean_wind_speed(self):
    #     wind_speed = self.cleaned_data.get('wind_speed')
    #     if not (0 <= wind_speed <= 150):
    #         raise forms.ValidationError("Wind speed must be between 0 and 150 m/s.")
    #     return wind_speed
