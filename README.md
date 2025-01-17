# CampWeatherSentry

#### Video Demo: https://youtu.be/upE2G_i4g5c

## Description

**CampWeatherSentry** is a command-line interface application designed for weather monitoring and analysis in Army Camps in Singapore!

It uses [OpenWeather](https://openweathermap.org/)'s API to get its weather data.

## How do I run this programme?
1. Have a Python environment running. I used the version 3.11.8 to develop this. Download [Python 3.11.8 here](https://www.python.org/downloads/release/python-3118/).
2. Clone this repository into a command-line interface (such as bash) by running
   ```bash
   git clone https://github.com/fiftypeachy/CampWeatherSentry-Public.git
   ```
3. and cd into the cloned repository by executing
   ```bash
   cd CampWeatherSentry-Public
   ```
4. Execute
   ```bash
   pip install -r requirements.txt
   ```
   to install the necessary dependencies.
5. Execute
   ```bash
   export API_KEY_WEATHER=<API_KEY>
   ```
   substituting the *<API_KEY>* with the actual API_KEY (in the supporting document).
6. Execute
   ```bash
   python project.py
   ```
   to run the programme!

## Motivation behind Project

As the Singapore Armed Forces operates as a conscript army, ensuring training safety becomes significantly more paramount. Convenient access to weather data addresses one of the safety concerns, particularly mitigating risks associated with extreme temperatures and lightning hazards. This application aims to equip soldiers with forecasted weather information to anticipate potential concerns during training sessions.

## Development Process

Prior to writing the main bulk of the application, I needed to gather the list of camps and their corresponding latitude (lat) and longitude (lng). This is because OpenWeather's API wants us to provide as inputs the lat and lng.

To achieve this, I used one of Google Map's APIs called Geocoding API, where I input place names (which are army camps in this context) and called the API to obtain the lat and lng for the respective camps. This is written in [get_camp_coords.py](get_camp_coords.py).

## How does the application run?

Firstly, the user is prompted to provide the name of the camp that they are interested in getting the weather data for. This is written in [filtering_camps.py](filtering_camps.py) The application then uses [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/) to fuzzy string match the user's input, allowing me to compare the string similarity rather than equality. 

Thereafter, this camp's latitude and longitude are being searched for through the "database" in the form of a CSV file, [camps_data.csv](camps_data.csv) generated by [get_camp_coords.py](get_camp_coords.py).

Next, I called upon OpenWeather's API to get weather data for that particular location, and the data is being parsed using the function `convert_to_dataframe(data)`. The final way the information is parsed is in the form of three dataframes, for the three aspects — Probability of rain, Forecasted weather description and Cloud cover. Each table shows weather forecasted data 5 days from today. 

Finally, I formatted the parsed data with colours and printed it out.

## Possible future improvements
1. I could work on daily temperature Highs and Lows.
2. Integrate with internal Lightning Warning Systems.
3. Write it in a more user-friendly UI such as in a webpage.
4. Display the data in an interactive map to improve user experience.
5. I could scale the project up to enable users to search for forecasts anywhere in Singapore, which calls upon Google Maps API every time a new location is searched to get its corresponding latitude and longitude.

## Acknowledgments
### Weather Data
The weather data used in this project is provided by [OpenWeather](https://openweathermap.org/).

### Geocoding Data
The latitudes and longitudes data used in this project is provided by [Google](https://developers.google.com/maps/documentation/geocoding).
