import base64
import os
import requests
from datetime import date, timedelta

TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class AmadeusClient:
    def __init__(self):
        self.client_id = os.environ["AMADEUS_CLIENT_ID"]
        self.client_secret = os.environ["AMADEUS_CLIENT_SECRET"]
        self.session = requests.Session()
        self.token = self._get_token()

    def _get_token(self):
        response = self.session.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def search(self, origin, destination, departure, return_date):
        response = self.session.get(
            SEARCH_URL,
            headers={"Authorization": f"Bearer {self.token}"},
            params={
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure.isoformat(),
                "returnDate": return_date.isoformat(),
                "adults": 1,
                "travelClass": "ECONOMY",
                "currencyCode": "EUR",
                "max": 20,
            },
            timeout=45,
        )
        response.raise_for_status()
        return response.json().get("data", [])
