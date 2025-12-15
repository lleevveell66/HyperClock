#!/usr/bin/env python
####################################################
# get_moon_data.py v4.0 by level6 of LiE
####################################################
"""
This module will calculate moonrise and moonset times for
any given latitude, longitude
"""

from datetime import date, datetime, timezone
import skyfield  # apt -y install python3-skyfield
from skyfield.api import load, wgs84
from skyfield.data import hipparcos
import numpy as np

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
    t0 = ts.utc(today.year, today.month, today.day)

    # Load the ephemeris data
    eph = load('de421.bsp')  # This is a standard ephemeris file
    earth = eph['earth']
    moon = eph['moon']

    # Define the observer's location
    location = earth + wgs84.latlon(latitude, longitude)

    # Create a time series for the day
    times = ts.utc(today.year, today.month, today.day, 0, 0, 0)  # Start of the day
    time_steps = 1440  # Number of 1-minute steps in a day
    time_delta = ts.utc(0, 0, 0, 0, 1, 0)  # 1-minute delta
    times_series = [times + i * time_delta for i in range(time_steps)]

    # Calculate altitudes for each time
    altitudes = []
    for time in times_series:
        alt, az, dist = location.at(time).observe(moon).apparent().altaz()
        altitudes.append(alt.degrees)

    # Find moonrise and moonset times
    moonrise_time = None
    moonset_time = None
    for i in range(len(altitudes) - 1):
        if altitudes[i] < 0 and altitudes[i + 1] > 0:
            # Linear interpolation for moonrise
            time_diff = times_series[i+1] - times_series[i]
            fraction = abs(altitudes[i]) / (altitudes[i+1] - altitudes[i])
            moonrise_time = times_series[i] + fraction * time_diff
        elif altitudes[i] > 0 and altitudes[i + 1] < 0:
            # Linear interpolation for moonset
            time_diff = times_series[i+1] - times_series[i]
            fraction = altitudes[i] / (altitudes[i+1] - altitudes[i])
            moonset_time = times_series[i] + fraction * time_diff

    if moonrise_time and moonset_time:
        return moonrise_time.utc_datetime(), moonset_time.utc_datetime()
    else:
        return None, None
