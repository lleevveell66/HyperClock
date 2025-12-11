#!/usr/bin/env python
##########################################################
# hyper_config.py v4.0 by level6
# https://github.com/lleevveell66/HyperClock
##########################################################

"""
Read in HyperClock configuration information from HyperClock.conf
"""

import sys
import configparser

CONFIG_FILE='/usr/local/HyperClock/conf/hyper_clock.conf'

def debug_print(string_to_print):
    """
    This function will print the supplied string_to_print, if debug_on is True
    """

    if debug_on:
        print(string_to_print)

config=configparser.ConfigParser()

try:
    config.read(CONFIG_FILE)

except FileNotFoundError:
    print("Error: The file {CONFIG_FILE} was not found")
    sys.exit(1)
except PermissionError:
    print("Error: Permission denied to read: {CONFIG_FILE}")
    sys.exit(1)
except UnicodeDecodeError:
    print("Error: Could not decode file: {CONFIG_FILE} .  Check encoding.")
    sys.exit(1)
except IOError as other_error:    # Catch other IO errors
    print(f"IOError: {other_error}")
    sys.exit(1)


cfg_topology=config.get('HyperClock','topology')
cfg_weather_data_file=config.get('HyperClock','weather_data_file')
cfg_weather_data_command=config.get('HyperClock','weather_data_command')
cfg_indoor_temp_file=config.get('HyperClock','indoor_temp_file')
cfg_indoor_temp_command=config.get('HyperClock','indoor_temp_command')
cfg_zip_code=config.get('HyperClock','zip_code')
cfg_units=config.get('HyperClock','units')
cfg_debug_on=config.get('HyperClock','debug_on')
cfg_syslog_on=config.get('HyperClock','syslog_on')
cfg_hour_24=config.get('HyperClock','hour_24')
cfg_time_font=config.get('HyperClock','time_font')
cfg_date_font=config.get('HyperClock','date_font')
cfg_weather_font=config.get('HyperClock','weather_font')
cfg_temp_font=config.get('HyperClock','temp_font')
cfg_indoor_temp_font=config.get('HyperClock','indoor_temp_font')
cfg_high_font=config.get('HyperClock','high_font')
cfg_low_font=config.get('HyperClock','low_font')
cfg_forecast_font=config.get('HyperClock','forecast_font')
cfg_wind_font=config.get('HyperClock','wind_font')
cfg_pressure_font=config.get('HyperClock','pressure_font')
cfg_humidity_font=config.get('HyperClock','humidity_font')
cfg_sunriseset_font=config.get('HyperClock','sunriseset_font')
cfg_moonriseset_font=config.get('HyperClock','moonriseset_font')
cfg_last_font=config.get('HyperClock','last_font')
cfg_time_color=config.get('HyperClock','time_color')
cfg_date_color=config.get('HyperClock','date_color')
cfg_weather_color=config.get('HyperClock','weather_color')
cfg_temp_color=config.get('HyperClock','temp_color')
cfg_indoor_temp_color=config.get('HyperClock','indoor_temp_color')
cfg_high_color=config.get('HyperClock','high_color')
cfg_low_color=config.get('HyperClock','low_color')
cfg_wind_color=config.get('HyperClock','wind_color')
cfg_pressure_color=config.get('HyperClock','pressure_color')
cfg_humidity_color=config.get('HyperClock','humidity_color')
cfg_day1_color=config.get('HyperClock','day1_color')
cfg_day2_color=config.get('HyperClock','day2_color')
cfg_day3_color=config.get('HyperClock','day3_color')
cfg_day4_color=config.get('HyperClock','day4_color')
cfg_sunrise_color=config.get('HyperClock','sunrise_color')
cfg_sunset_color=config.get('HyperClock','sunset_color')
cfg_moonrise_color=config.get('HyperClock','moonrise_color')
cfg_moonset_color=config.get('HyperClock','moonset_color')
cfg_last_color=config.get('HyperClock','last_color')

debug_on = cfg_debug_on

debug_print(" ")
debug_print(" ")
debug_print("I have read the following configuration from /usr/local/HyperClock/HyperClock.conf :")
debug_print(f"             Topology: {cfg_topology}")
debug_print(f"    Weather Data File: {cfg_weather_data_file}")
debug_print(f" Weather Data Command: {cfg_weather_data_command}")
debug_print(f"     Indoor Temp File: {cfg_indoor_temp_file}")
debug_print(f"  Indoor Temp command: {cfg_indoor_temp_command}")
debug_print(" ")
debug_print(" ")
