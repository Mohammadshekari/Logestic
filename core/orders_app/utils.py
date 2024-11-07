import requests
from datetime import datetime
from django.conf import settings
import googlemaps



class Nominatim:

    @staticmethod
    def get_lat_lon(zip_code):
        url = "https://nominatim.openstreetmap.org/search"
        headers = {
            "User-Agent": "YourAppName/1.0 (your_email@example.com)",
            "Referer": "https://yourwebsite.com/"
        }
        params = {
            "postalcode": zip_code,
            "format": "json"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if len(data) > 0:
            location = data[0]
            return float(location['lat']), float(location['lon'])
        else:
            return None

    @staticmethod
    def get_point(zip_code):
        url = "https://nominatim.openstreetmap.org/search"
        headers = {
            "User-Agent": "YourAppName/1.0 (your_email@example.com)",
            "Referer": "https://yourwebsite.com/"
        }
        params = {
            "postalcode": zip_code,
            "format": "json"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if len(data) > 0:
            location = data[0]
            return {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "coordinates": [float(location['lat']), float(location['lon'])],
                    "type": "Point"
                }
            }
        else:
            return None


ZipCodeConverter = Nominatim



def calculate_google_map_distance(order_instance):
    try:
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_API_TOKEN)
        origin = order_instance.order_origin.location_point.coords # Example: Colosseum in Rome
        destination = order_instance.order_destination.location_point.coords # Example: Palermo in Sicily

        # Request directions
        directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())

        # Extract distance from the directions result
        if directions_result and 'legs' in directions_result[0]:
            distance_meters = directions_result[0]['legs'][0]['distance']['value']
            distance = distance_meters / 1000
            order_instance.google_map_distance = distance
            order_instance.save()
    except:
        raise