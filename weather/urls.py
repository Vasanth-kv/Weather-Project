from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from weather import views
from weather.views import WeatherViewSet, fetch_and_store_weather, get_weather_data

# Create a simple view for the root URL
def home(request):
    print("Request received!")  # Add this log
    return HttpResponse("Welcome to the Weather Project! Use /weather for the API.")

router = DefaultRouter()
router.register(r'weather', WeatherViewSet)

urlpatterns = [
    path('api/weather/', fetch_and_store_weather, name='fetch_and_store_weather'),
    path('api/weather/', get_weather_data, name='get_weather_data'),  # This handles the GET request
    # path('create_weather/', create_weather_entry, name='create_weather'),
    # path('get_weather/', get_weather_by_location_and_date, name='get_weather_by_location_and_date'),
    # path('get_weather_list/', get_weather_by_location, name='get_weather_by_location'),

    path('', include(router.urls)),
]
