#!/usr/bin/env python
####################################################
# get_weather_data_local.py v4.0 by level6 of LiE
####################################################

"""
THIS SCRIPT IS TOTALLY BROKEN, RIGHT NOW.

This script will get weather data locally
"""

import datetime
import sys
import urllib
import math
import decimal
import syslog

from datetime import datetime
from xml.dom import minidom
from xml.dom.minidom import Document

import hyper_config

dec=decimal.Decimal

zip_code=hyper_config.cfg_zip_code

WURL='https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20zip_code%3D'+str(zip_code)
WSER='http://xml.weather.yahoo.com/ns/rss/1.0'

def position(now=None):
    """
    Unsure...
    """

    if now is None:
        now = datetime.now()

    diff = now - datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))

    return lunations % dec(1)

def phase(pos):
    """
    Returns the moon phase name based on position
    """

    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    return {
        0: "New Moon",
        1: "Waxing Crescent",
        2: "First Quarter",
        3: "Waxing Gibbous",
        4: "Full Moon",
        5: "Waning Gibbous",
        6: "Last Quarter",
        7: "Waning Crescent"
    }[int(index) & 7]

def phase_num(pos):
    """
    Returns the moon phase number based on position
    """

    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    return {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7"
    }[int(index) & 7]

def get_weather():
    """
    Gets the weather for a weoid
    """

    url=WURL

    try:
        dom=minidom.parse(urllib.urlopen(url))
    except:
        parse_error=sys.exc_info()[0]
        print("Error: %s" % parse_error)
        syslog.syslog(syslog.LOG_ERR,"Error: %s" % parse_error)

    forecasts = []
    for node in dom.getElementsByTagNameNS(WSER, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'day': node.getAttribute('day'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text'),
            'code': node.getAttribute('code')
        })
    ycondition=dom.getElementsByTagNameNS(WSER,'condition')[0]
    yatmosphere=dom.getElementsByTagNameNS(WSER,'atmosphere')[0]
    ywind=dom.getElementsByTagNameNS(WSER,'wind')[0]
    yastronomy=dom.getElementsByTagNameNS(WSER,'astronomy')[0]
    return {
        'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'current_code': ycondition.getAttribute('code'),
        'forecasts': forecasts ,
        'humidity': yatmosphere.getAttribute('humidity'),
        'pressure': yatmosphere.getAttribute('pressure'),
        'rising': yatmosphere.getAttribute('rising'),
        'wind_direction': ywind.getAttribute('direction'),
        'wind_speed': ywind.getAttribute('speed'),
        'wind_chill': ywind.getAttribute('chill'),
        'sunrise': yastronomy.getAttribute('sunrise'),
        'sunset': yastronomy.getAttribute('sunset'),
        }


def download_and_write_weather(zip_code):
    """
    Downloads the weather for a zip_code
    """

    # seconds=int(datetime.now().strftime("%s"))
    current_time=datetime.now().strftime("%I:%M %p")

    current_date=datetime.now().strftime("%A %m/%d/%Y")

    try:
        weather=get_weather()
    except:
        weather_error=sys.exc_info()[0]
        print(f"Error: %s" % weather_error)
        syslog.syslog(syslog.LOG_ERR,f"Error: %s" % weather_error)

    current_condition=weather['current_condition']
    current_temp=weather['current_temp']
    current_code=weather['current_code']
    humidity=weather['humidity']
    pressure=weather['pressure']
    rising=weather['rising']
    wind_direction=weather['wind_direction']
    wind_speed=weather['wind_speed']
    wind_chill=weather['wind_chill']
    sunrise=weather['sunrise']
    sunset=weather['sunset']

    get_indoor_temp_cmd="/var/www/html/BERTHA/therm.py -q | grep CurrentTemp | sed 's/CurrentTemp //'"
    # IndoorTemp=subprocess.check_output('{}'.format(getIndoorTempCmd),shell=True)
    #IndoorTemp=subprocess.Popen(format(getIndoorTempCmd),shell=True)
    indoor_temp="NA"

    get_indoor_setting_cmd="/var/www/html/BERTHA/therm.py -q | grep CoolSetpoint | sed 's/CoolSetpoint //'"
    # IndoorSetting=subprocess.check_output('{}'.format(getIndoorSettingCmd),shell=True)
    #IndoorSetting=subprocess.Popen(format(getIndoorSettingCmd),shell=True)
    indoor_setting="NA"

    day0_date=weather['forecasts'][0]['date']
    day0_day=weather['forecasts'][0]['day']
    day0_high=weather['forecasts'][0]['high']
    day0_low=weather['forecasts'][0]['low']
    day0_code=weather['forecasts'][0]['code']
    day0_condition=weather['forecasts'][0]['condition']
    day1_date=weather['forecasts'][1]['date']
    day1_day=weather['forecasts'][1]['day']
    day1_high=weather['forecasts'][1]['high']
    day1_low=weather['forecasts'][1]['low']
    day1_code=weather['forecasts'][1]['code']
    day1_condition=weather['forecasts'][1]['condition']
    day2_date=weather['forecasts'][2]['date']
    day2_day=weather['forecasts'][2]['day']
    day2_high=weather['forecasts'][2]['high']
    day2_low=weather['forecasts'][2]['low']
    day2_code=weather['forecasts'][2]['code']
    day2_condition=weather['forecasts'][2]['condition']
    day3_date=weather['forecasts'][3]['date']
    day3_day=weather['forecasts'][3]['day']
    day3_high=weather['forecasts'][3]['high']
    day3_low=weather['forecasts'][3]['low']
    day3_code=weather['forecasts'][3]['code']
    day3_condition=weather['forecasts'][3]['condition']
    day4_date=weather['forecasts'][4]['date']
    day4_day=weather['forecasts'][4]['day']
    day4_high=weather['forecasts'][4]['high']
    day4_low=weather['forecasts'][4]['low']
    day4_code=weather['forecasts'][4]['code']
    day4_condition=weather['forecasts'][4]['condition']

    doc=Document()
    data=doc.createElement('data')
    doc.appendChild(data)

    now=doc.createElement('now')
    now.setAttribute("date",current_date)
    now.setAttribute("time",current_time)
    data.appendChild(now)

    astral=doc.createElement('astral')
    astral.setAttribute("sunrise",sunrise)
    astral.setAttribute("sunset",sunset)

    pos=position()
    moon_phase_name=phase(pos)
    moon_phase_num=phase_num(pos)

    astral.setAttribute("moon_phase",moon_phase_name)
    astral.setAttribute("moon_phase_num",moon_phase_num)
    data.appendChild(astral)

    weather=doc.createElement('weather')
    data.appendChild(weather)
    current=doc.createElement('current')
    weather.appendChild(current)
    current.setAttribute("temp",current_temp)
    current.setAttribute("humidity",humidity)
    current.setAttribute("pressure",pressure)
    current.setAttribute("rising",rising)
    current.setAttribute("wind_direction",wind_direction)
    current.setAttribute("wind_speed",wind_speed)
    current.setAttribute("wind_chill",wind_chill)
    current.setAttribute("condition",current_condition)
    current.setAttribute("code",current_code)
    current.setAttribute("indoor",indoor_temp)
    current.setAttribute("setting",indoor_setting)
    today=doc.createElement('today')
    today.setAttribute("high",day0_high)
    today.setAttribute("low",day0_low)
    forecast=doc.createElement('forecast')
    weather.appendChild(forecast)
    day0=doc.createElement('day0')
    day0.setAttribute("date",day0_date)
    day0.setAttribute("day",day0_day)
    day0.setAttribute("high",day0_high)
    day0.setAttribute("low",day0_low)
    day0.setAttribute("code",day0_code)
    day0.setAttribute("precip",'100')
    day0.setAttribute("condition",day0_condition)
    day1=doc.createElement('day1')
    day1.setAttribute("date",day1_date)
    day1.setAttribute("day",day1_day)
    day1.setAttribute("high",day1_high)
    day1.setAttribute("low",day1_low)
    day1.setAttribute("code",day1_code)
    day1.setAttribute("precip",'100')
    day1.setAttribute("condition",day1_condition)
    day2=doc.createElement('day2')
    day2.setAttribute("date",day2_date)
    day2.setAttribute("day",day2_day)
    day2.setAttribute("high",day2_high)
    day2.setAttribute("low",day2_low)
    day2.setAttribute("code",day2_code)
    day2.setAttribute("precip",'100')
    day2.setAttribute("condition",day2_condition)
    day3=doc.createElement('day3')
    day3.setAttribute("date",day3_date)
    day3.setAttribute("day",day3_day)
    day3.setAttribute("high",day3_high)
    day3.setAttribute("low",day3_low)
    day3.setAttribute("code",day3_code)
    day3.setAttribute("precip",'100')
    day3.setAttribute("condition",day3_condition)
    day4=doc.createElement('day4')
    day4.setAttribute("date",day4_date)
    day4.setAttribute("day",day4_day)
    day4.setAttribute("high",day4_high)
    day4.setAttribute("low",day4_low)
    day4.setAttribute("code",day4_code)
    day4.setAttribute("precip",'100')
    day4.setAttribute("condition",day4_condition)
    forecast.appendChild(day0)
    forecast.appendChild(day1)
    forecast.appendChild(day2)
    forecast.appendChild(day3)
    forecast.appendChild(day4)
    data.appendChild(weather)

    doc.writexml(open(hyper_config.cfg_weather_data_file,"wb"),indent="  ",addindent="  ",newl='\n')

    doc.unlink()
