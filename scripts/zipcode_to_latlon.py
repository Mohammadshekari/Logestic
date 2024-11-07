import requests


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
            return location['lat'], location['lon']
        else:
            return None

class Google:
    api_key = 'AIzaSyBY0p81Zhi8Iu00wWTw8GToyuRgsohB_pE'
    def get_lat_lon(zip_code):
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": f"zip_code {zip_code}",
            "key":__class__.api_key
        }
        response = requests.get(url,params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        


zip_code = '20200'
lat, lon = Google.get_lat_lon(zip_code)
print(lat, lon)

