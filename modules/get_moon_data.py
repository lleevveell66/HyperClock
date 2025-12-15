#!/usr/bin/env python
####################################################
# get_moon_data.py v4.0 by level6 of LiE
####################################################
"""
This module will calculate moonrise and moonset times for
any given latitude, longitude
"""

import datetime
import ephem

def calculate_moonrise_moonset(latitude, longitude):
    """
    Calculates moonrise and mooset basd on local date and lat/lon and
    returns them in HH:MM AM/PM format.
    """

    # Create an observer at the specified latitude and longitude
    observer = ephem.Observer()
    observer.lon = str(longitude)
    observer.lat = str(latitude)

    # Get the current date and time
    now = datetime.datetime.now()

    # Calculate the moon's position at the current time
    moon = ephem.Moon()
    moon.compute(observer)

    # Calculate the moonrise and moonset times
    moonrise = observer.previous_rising(moon, start=now)
    moonset = observer.next_setting(moon, start=now)

    return (datetime.timedelta(days=moonrise).strftime("%I:%M %p"), datetime.timedelta(days=moonset).strftime("%I:%M %p"))
