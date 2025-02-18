from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

class Weather(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()

    def __str__(self):
        return f"{self.city} - {self.date}"
    
    def clean(self):
        # Validate city
        if not self.city or not self.city.strip():
            raise ValidationError({"city": "City cannot be empty."})

        # Validate date (should not be in the future)
        if self.date > datetime.now().date():
            raise ValidationError({"date": "The date cannot be in the future."})

        # Validate temperature range
        if not (-100 <= self.temperature <= 60):
            raise ValidationError({"temperature": "Temperature must be between -100 and 60 degrees Celsius."})

        # Validate humidity range
        if not (0 <= self.humidity <= 100):
            raise ValidationError({"humidity": "Humidity must be between 0 and 100 percent."})

        # Validate wind speed range
        if not (0 <= self.wind_speed <= 150):
            raise ValidationError({"wind_speed": "Wind speed must be between 0 and 150 m/s."})

    def save(self, *args, **kwargs):
        # Ensure data is validated before saving
        self.clean()
        super().save(*args, **kwargs)
