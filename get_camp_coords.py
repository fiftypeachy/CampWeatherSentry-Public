import csv
import os

import googlemaps
from googlemaps.exceptions import *

from list_of_camp_names import camps

"""Using Google Maps Geocoding API, I give it the name of the camp, 
and process the data to return a csv file named "camps_data.csv" with 
headers name, lat, lng."""

gmaps_api_key = os.environ.get("API_KEY_GOOGLEMAPS")
gmaps = googlemaps.Client(key=gmaps_api_key)

csv_file = "camps_data.csv"

with open(csv_file, mode="w") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "lat", "lng"])

    # Write header
    writer.writeheader()

    for camp in camps:
        # Geocode camp address
        try:
            geocode_result = gmaps.geocode(camp)
        except ApiError as e:
            print("An API error occurred:", e)

        except HTTPError as e:
            print("An HTTP error occurred:", e)

        except Timeout:
            print("The request timed out.")

        except TransportError as e:
            print("A transport error occurred:", e)

        if not geocode_result:
            continue

        lat, lng = geocode_result[0]["geometry"]["location"].values()

        writer.writerow({"name": camp, "lat": lat, "lng": lng})
