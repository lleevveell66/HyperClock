#!/usr/bin/env python
####################################################
# get_moon_data.py v4.0 by level6 of LiE
####################################################

"""
This module will calculate moonrise and moonset times for
any given latitude, longitude
"""

from datetime import date, datetime, timezone

import skyfield                    # apt -y install python3-skyfield

from skyfield.api import load, wgs84
from skyfield.data import hipparcos

def calculate_moonrise_moonset(latitude, longitude):
    """
    Calculates the moonrise and moonset times for a given location and date.

    Args:
        latitude (float): Latitude in degrees.
        longitude (float): Longitude in degrees.

    Returns:
        tuple: A tuple containing the moonrise and moonset times as datetime objects,
               or (None, None) if the calculation fails.
    """

    today = datetime.now()

    ts = load.timescale()
    t = ts.utc(today.year, today.month, today.day)

    # Load the ephemeris data
    eph = load('de421.bsp')  # This is a standard ephemeris file
    earth = eph['earth']
    moon = eph['moon']

    # Define the observer's location
    location = earth + wgs84.latlon(latitude, longitude)

    # Calculate apparent altitude of the moon
    altitudes = location.at(t).observe(moon).apparent().altaz()

    # Find the times when the moon crosses the horizon (0 degrees altitude)
    horizon_crossing_times = []
    for i in range(len(altitudes) - 1):
        if altitudes[i].degrees < 0 and altitudes[i+1].degrees > 0:
            horizon_crossing_times.append(t + (altitudes[i+1].t - altitudes[i].t) * (0 - altitudes[i].degrees) / (altitudes[i+1].degrees - altitudes[i].degrees))
        elif altitudes[i].degrees > 0 and altitudes[i+1].degrees < 0:
            horizon_crossing_times.append(t + (altitudes[i+1].t - altitudes[i].t) * (0 - altitudes[i].degrees) / (altitudes[i+1].degrees - altitudes[i].degrees))

    # moonrise_datetime = int(data["current"]["moonrise"])                
    # # Convert timestamp to datetime object                
    # dt_object = datetime.fromtimestamp(moonrise_datetime)                
    # # Format the time                
    # new_moonrise = dt_object.strftime("%I:%M %p")
    # 
    # moonset_datetime = int(data["current"]["moonset"])                          
    # # Convert timestamp to datetime object                         
    # dt_object = datetime.fromtimestamp(moonset_datetime)                
    # # Format the time                       
    # new_moonset = dt_object.strftime("%I:%M %p")                

    if len(horizon_crossing_times) >= 2:
        moonrise_time = horizon_crossing_times[0].utc_datetime()
        moonset_time = horizon_crossing_times[1].utc_datetime()
        return moonrise_time, moonset_time
    else:
        return None, None  # Could not calculate moonrise/moonset
