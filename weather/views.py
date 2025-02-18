from venv import logger
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,viewsets
from .models import Weather
from .serializers import WeatherSerializer
from weather_api import get_weather
from datetime import datetime

class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    
@api_view(['POST'])
def fetch_and_store_weather(request):
    """Fetch weather data from external API and save it to the database."""
    city = request.data.get('city')
    date = request.data.get('date', datetime.utcnow().date())  # Default to today if no date provided

    if not city:
        return Response({"error": "City is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch data from OpenWeatherMap API
        weather_data = get_weather(city)
        if not weather_data:
            return Response({"error": "Failed to fetch weather data."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract relevant details
        weather_details = {
            "city": city,
            "date": datetime.utcfromtimestamp(weather_data["dt"]).date(),
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data["wind"]["speed"],
        }

        # Save data to the database (avoid duplicates)
        existing_record = Weather.objects.filter(city=city, date=weather_details["date"]).first()
        if existing_record:
            return Response({"message": "Weather data for this city and date already exists."}, status=status.HTTP_200_OK)

        serializer = WeatherSerializer(data=weather_details)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GET request to retrieve weather data based on location and date
@api_view(['GET'])
def get_weather_data(request):
    """Retrieve weather data from external API based on city."""
    city = request.query_params.get('city')
    
    if not city:
        return Response({"error": "City is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch data from OpenWeatherMap API using your weather_api function
        weather_data = get_weather(city)
        
        if not weather_data:
            return Response({"error": "Failed to fetch weather data."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract relevant weather details
        weather_details = {
            "name": weather_data.get("name", "N/A"),
            "temperature": weather_data["main"].get("temp", "N/A"),
            "condition": weather_data["weather"][0].get("description", "N/A"),
            "humidity": weather_data["main"].get("humidity", "N/A"),
            "wind_speed": weather_data["wind"].get("speed", "N/A"),
        }

        return Response(weather_details, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        # Log the specific error if there's a failure with the external API request
        logger.error(f"Error fetching weather data: {e}")
        return Response({"error": f"Error fetching weather data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # Catch all other exceptions
        logger.error(f"Unexpected error: {e}")
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create weather entry
# @api_view(['POST'])
# def create_weather_entry(request):
#     serializer = WeatherSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Get weather by location and date
# @api_view(['GET'])
# def get_weather_by_location_and_date(request):
#     city = request.query_params.get('city')
#     date = request.query_params.get('date')
#     if not city or not date:
#         return Response({"error": "Both 'city' and 'date' parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         weather = Weather.objects.get(city=city, date=date)
#         serializer = WeatherSerializer(weather)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Weather.DoesNotExist:
#         return Response({"error": "No weather data found for the given city and date."}, status=status.HTTP_404_NOT_FOUND)

# # Get all weather details for a location
# @api_view(['GET'])
# def get_weather_by_location(request):
#     city = request.query_params.get('city')
#     if not city:
#         return Response({"error": "'city' parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
#     weather_entries = Weather.objects.filter(city=city)
#     if weather_entries.exists():
#         serializer = WeatherSerializer(weather_entries, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({"error": "No weather data found for the given city."}, status=status.HTTP_404_NOT_FOUND)

