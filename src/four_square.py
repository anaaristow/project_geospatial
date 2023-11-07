import requests
import json
import pandas as pd
from getpass import getpass
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd

def find_venue(lat, lon, password, query, radius=500, limit=50):
    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={lat}%2C{lon}&radius={radius}&limit={limit}"
    headers = {
        "accept": "application/json",
        "Authorization": password
    }
    try:
        response = requests.get(url, headers=headers).json()
        #print(response)
        venues = response.get('results', [])
        #print(venues)
        return len(venues)
    except:
        print("no :(")

def count_venues_per_neighborhood(neighborhood_coordinates, password, query, radius):
    results = {} 
    for neighborhood, coordinates in neighborhood_coordinates.items():
        lat = coordinates['Latitude']
        lon = coordinates['Longitude']
        count = find_venue(lat, lon, password=password, query=query, radius=500, limit=50)
        results[neighborhood] = count

    df = pd.DataFrame(list(results.items()), columns=["Neighborhood",  query])
    return df



