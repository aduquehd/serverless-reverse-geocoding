import os
import json
import urllib.request


class GoogleGeocodeAPI:
    def __init__(self):
        self.API_KEY = os.environ['GOOGLE_GEOCODING_API_KEY']
        self.url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_geocode(self, latitude, longitude):
        url = f'{self.url}?latlng={latitude},{longitude}'
        return self.get_api_data(url)

    def get_reverse_geocode(self, address):
        url = f'{self.url}?address={address}'
        return self.get_api_data(url)

    def get_api_data(self, url):
        url = self._apply_api_key(url)
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())

    def _apply_api_key(self, url):
        return f'{url}&key={self.API_KEY}'
