import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_nearby_hospitals(lat: float, lng: float):
    """Finds hospitals within 5km of the user's coordinates."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        # Return a simple list of names and addresses for Nipun's UI
        return [{"name": r["name"], "address": r.get("vicinity")} for r in results[:5]]
    return []