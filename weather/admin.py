from django.contrib import admin
from .models import Weather

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'temperature', 'humidity', 'wind_speed')
    # search_fields = ('city',)  # Adds a search bar for city
    # list_filter = ('date', 'city')  # Adds filters for date and city
    # ordering = ('-date',)  # Orders the data by date in descending order

