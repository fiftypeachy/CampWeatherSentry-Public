import csv
import datetime
import os
import sys

import pandas as pd
import requests
from tabulate import tabulate

from filtering_camps import handle_user_input

# ANSI escape codes for formatted text
bold = "\033[1m"
underline = "\033[4m"
end = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
white = "\033[97m"


def get_openweather_api_key():
    api_key = os.environ.get("API_KEY_WEATHER")

    if api_key:
        print("API key:", "*" * len(api_key))
    else:
        print("API key not found. Make sure it's set in your environment.")
        sys.exit()

    return api_key


def main():
    print(
        f"{bold}Hello! This is CampWeatherSentry, where you can get updates on weather in SG Army Camps!{end}"
    )

    print(f"{bold}Search for a camp ------>{end}")

    camp_name = handle_user_input()

    lat, lng = get_lat_lng(camp_name)

    if not lat or not lng:
        sys.exit("Camp is probably temporarily or permanently closed.")

    api_key = get_openweather_api_key()

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&units=metric&appid={api_key}"

    response = requests.get(url)

    if response.status_code != 200:
        sys.exit("Check your internet connection and try again.")

    data = response.json()

    print(f"{bold}{underline}Showing results for {green}{camp_name}{white}.{end}")
    print()

    convert_to_dataframe(data)


def get_lat_lng(camp_name):
    filename = "camps_data.csv"
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if camp_name == row["name"]:
                return row["lat"], row["lng"]

        return None, None


def convert_to_dataframe(data):

    todays_date = datetime.datetime.now().date()
    table = {}

    for d in data["list"]:
        time_being_forecasted = datetime.datetime.fromtimestamp(d["dt"])
        weather = d["weather"][0]["description"]
        cloudiness = d["clouds"]["all"]  # in percentage
        pop = int(d["pop"] * 100)
        colour = red if pop > 80 else yellow if 50 <= pop <= 80 else green

        aspects = [
            f"{colour}{pop}%{white}",
            f"{weather.title()}",
            f"{parse_cloudiness(cloudiness)}",
        ]
        table.update({time_being_forecasted: aspects})

    next_6_days = [
        (todays_date + datetime.timedelta(days=i)).strftime("%A") for i in range(6)
    ]
    time_of_day = [
        t.strftime("%-I%p") for t in sorted(set(key.time() for key in table))
    ]

    dataframes = [
        pd.DataFrame(index=time_of_day, columns=next_6_days),
        pd.DataFrame(index=time_of_day, columns=next_6_days),
        pd.DataFrame(index=time_of_day, columns=next_6_days),
    ]

    for t in table:
        day = t.strftime("%A")
        time = t.time().strftime("%-I%p")
        for i in range(3):
            df = dataframes[i]
            df.loc[time, day] = table[t][i]

    for df in dataframes:
        df.fillna("-", inplace=True)

    aspect_titles = ["Probability of rain:", "Forecasted weather type:", "Cloud cover:"]
    for i in range(3):
        print(f"{bold}{aspect_titles[i]}{end}")
        print(tabulate(dataframes[i], headers="keys", tablefmt="fancy_grid"))
        print()


def parse_cloudiness(cloud_cover):
    if 0 <= cloud_cover < 11:
        return "Little Cloud Cover"
    elif 11 <= cloud_cover <= 25:
        return "Few Clouds"
    elif 25 < cloud_cover <= 50:
        return "Scattered Clouds"
    elif 50 < cloud_cover <= 85:
        return "Broken Clouds"
    elif 85 < cloud_cover <= 100:
        return "Overcast Clouds"


if __name__ == "__main__":
    main()
