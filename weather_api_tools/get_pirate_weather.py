#!/usr/bin/python
#################################################################
# get_pirate_weather v0.0 by level6 of LiE
# -----------------------------------------------

"""
# This script will take a zip code as argument and return the
# lat/long coordinates in a JSON structure, similar to:
#
# {
#   "zip": "77338",
#   "name": "Humble",
#   "lat": 30.0041,
#   "lon": -95.2825,
#   "country": "US"
# }
#
# You need to subscribe to a free API on openweathermap.org
# and add it to the file: /usr/local/etc/api_keys.txt .  It needs
# to be in the following format:
#
# owm_api = <YOUR_OPENWEATHERMAP_API>
"""

#################################################################

import sys
import json
import csv
import requests

##########################################################
# Functions
##########################################################

def geo_from_zip(zcode):
    """
    This function will return latitude and longitude for the supplied zip code
    """

    try:
        with open("/usr/local/HyperClock/data/zipgeo.csv",'r',encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)               # Skip header

            for row in reader:
                if len(row) >= 3:
                    if row[0] == zcode:
                        try:
                            my_lat=float(row[1])
                            my_lon=float(row[2])
                            return my_lat, my_lon
                        except ValueError:
                            print(f"Invalid data for zipcode {zcode}")
                            return None, None
                else:
                    print(f"Skipping row with too few columns: {row}")
        return None, None
    except FileNotFoundError:
        print("File not found: /usr/local/HyperConfig/data/zipgeo.csv")
        return None, None
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        return None, None

def validate_zip(zip_code):
    """
    This function validates {zip_code} as a 5-digit numeric string and returns True or False
    """

    # Is it a string?
    if not isinstance(zip_code, str):
        return False

    # Is it 5 characters?
    if len(zip_code) != 5:
        return False

    # Is it all digits?
    if not zip_code.isdigit():
        return False

    # Seems ok
    return True

def read_api_key(file_path, api_name):
    """
    This function reads and returns your owm_api from {file_path} and returns
    the API key if found, None of not
    """

    try:
        with open(file_path,'r',encoding="utf-8") as open_file:
            for line in open_file:
                line=line.strip()  # remove leading/trailing whitespace
                if line.startswith(api_name + " = "):
                    parts=line.split(" = ")
                    if len(parts) == 2:
                        return parts[1].strip()  # return the API key
            print(f"Error: API '{api_name}' not found in {file_path}")
            return None

    except FileNotFoundError:
        print(f"Error: The {file_path} file was not found")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read: {file_path}")
        return None
    except UnicodeDecodeError:
        print(f"Error: Could not decode file: {file_path}.  Check encoding.")
        return None
    except IOError as other_error:    # Catch other IO errors
        print(f"IOError: {other_error}")
        return None

def get_pirate_weather_from_coords(api_key,lat,lon):
    """
    This function queries PirateWeather for information about {lat},{lon}
    using your {api_key} and returns the result as a JSON structure
    """

    units="imperial"
    exclude="hourly,minutely"
    api_url = f"https://api.pirateweather.net/forecast/{api_key}/{lat},{lon}"
    api_args = f"units={units}&exclude={exclude}"
    url = f"{api_url}?{api_args}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()

        return json.dumps(data)

    except requests.exceptions.RequestException as request_error:
        print(f"Request Error: {request_error}")
        return None
    except json.JSONDecodeError as decode_error:
        print(f"JSON Decode Error: {decode_error}")
        return None

def write_weather_data(weather_dict):
    """
    This function will extract what we need from {weather_dict}, convert
    it to a JSON string, and write it to data/weather_data.json
    """

    new_json_structure = {
          "current": {
            "datetime": weather_dict["currently"]["time"],
            "sunrise": weather_dict["daily"]["data"][0]["sunriseTime"],
            "sunset": weather_dict["daily"]["data"][0]["sunsetTime"],
            "temp": weather_dict["currently"]["temperature"],
            "temp_high": weather_dict["daily"]["data"][0]["temperatureHigh"],
            "temp_low": weather_dict["daily"]["data"][0]["temperatureLow"],
            "pressure": weather_dict["currently"]["pressure"],
            "humidity": weather_dict["currently"]["humidity"],
            "wind_speed": weather_dict["currently"]["windSpeed"],
            "wind_dir": weather_dict["currently"]["windBearing"],
            "moon_phase": weather_dict["daily"]["data"][0]["moonPhase"],
            "condition": weather_dict["currently"]["summary"],
            "icon": weather_dict["currently"]["icon"]
          },
          "daily": [
            {
              "datetime": weather_dict["daily"]["data"][1]["time"],
              "temp_high": weather_dict["daily"]["data"][1]["temperatureHigh"],
              "temp_low": weather_dict["daily"]["data"][1]["temperatureLow"],
              "icon": weather_dict["daily"]["data"][1]["icon"],
            },
            {
              "datetime": weather_dict["daily"]["data"][2]["time"],
              "temp_high": weather_dict["daily"]["data"][2]["temperatureHigh"],
              "temp_low": weather_dict["daily"]["data"][2]["temperatureLow"],
              "icon": weather_dict["daily"]["data"][2]["icon"],
            },
            {
              "datetime": weather_dict["daily"]["data"][3]["time"],
              "temp_high": weather_dict["daily"]["data"][3]["temperatureHigh"],
              "temp_low": weather_dict["daily"]["data"][3]["temperatureLow"],
              "icon": weather_dict["daily"]["data"][3]["icon"],
            },
            {
              "datetime": weather_dict["daily"]["data"][4]["time"],
              "temp_high": weather_dict["daily"]["data"][4]["temperatureHigh"],
              "temp_low": weather_dict["daily"]["data"][4]["temperatureLow"],
              "icon": weather_dict["daily"]["data"][4]["icon"],
            }
          ]
    }

    json_string=json.dumps(new_json_structure, indent=4)

    filename="/usr/local/HyperClock/data/weather_data.json"
    with open(filename,"w",encoding="utf-8") as weather_file:
        weather_file.write(json_string)

##########################################################
# Main Code
##########################################################

if __name__ == "__main__":

    # Was a command line argument supplied?
    if len(sys.argv)<2:
        # Nope.  Give them the syntax
        print("SYNTAX: ./get_pirate_weather.py <zip_code>")
        sys.exit(1)
    else:
        # Yep.  Must be a zip code, right?
        zip_arg=sys.argv[1]

        # Well, we should make sure
        if not validate_zip(zip_arg):
            print(f"Error: Invalid zip code: {zip_arg}.  Please supply only a 5-digit number.")
            sys.exit(1)

    pw_api_key=read_api_key("/usr/local/etc/api_keys.conf","pw_api")
    if pw_api_key is None:
        sys.exit(1)

    # geo_json = zip_info(owm_api_key,zip_arg)
    latitude, longitude = geo_from_zip(zip_arg)

    if latitude is None or longitude is None:
        print(f"Failed to get coordinates for zip {zip_arg}")
        sys.exit(1)

    # Get the JSON string repsonse
    weather_json = get_pirate_weather_from_coords(pw_api_key,latitude,longitude)

    if weather_json:
        # print(weather_json)

        # Turn the JSON string into a python dictionary
        this_weather_dict = json.loads(weather_json)

        # Get what we need and save it to data/weather_data.json
        write_weather_data(this_weather_dict)
    else:
        print(f"Error: Failed to get weather data for {latitude},{longitude}")

    # current_temp=weather_dict["current"]["temp"]
    # print(f"Current Temp: {current_temp}")

    #if geo_json:
    #    print(geo_json)
    #else:
    #    print("Failed to retreive zip code information.")
