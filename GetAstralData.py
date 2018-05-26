#!/usr/bin/env python

#import os, pygame, time, datetime, random, sys, urllib, math, decimal
import os, time, datetime, random, sys, urllib, math, decimal, subprocess, re, csv, syslog
import HyperConfig

from datetime import datetime
from xml.dom import minidom
from xml.dom.minidom import Document

dec=decimal.Decimal

# http://woeid.rosselliot.co.nz/
# http://woeid.factormystic.net/
woeid=HyperConfig.cfg_woeid

#wurl='http://xml.weather.yahoo.com/forecastrss?p=%s'
#wurl='http://weather.yahooapis.com/forecastrss?p=%s'
#wser='http://weather.yahooapis.com/ns/rss/1.0'
#wurl='https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D2480733'
wurl='https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%3D'+str(woeid)
wser='http://xml.weather.yahoo.com/ns/rss/1.0'

def position(now=None):
   if now is None:
      now = datetime.now()

   diff = now - datetime(2001, 1, 1)
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   return lunations % dec(1)

def phase(pos):
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

def phasenum(pos):
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

def getWeather(woeid):
	url=wurl

	try:
		dom=minidom.parse(urllib.urlopen(url))
	except:
                e=sys.exc_info()[0]
                print "Error: %s" % e
                syslog.syslog(syslog.LOG_ERR,"Error: %s" % e)
		
	forecasts = []
	for node in dom.getElementsByTagNameNS(wser, 'forecast'):
		forecasts.append({
			'date': node.getAttribute('date'),
			'day': node.getAttribute('day'),
			'low': node.getAttribute('low'),
			'high': node.getAttribute('high'),
			'condition': node.getAttribute('text'),
			'code': node.getAttribute('code')
		})
	ycondition=dom.getElementsByTagNameNS(wser,'condition')[0]
	yatmosphere=dom.getElementsByTagNameNS(wser,'atmosphere')[0]
	ywind=dom.getElementsByTagNameNS(wser,'wind')[0]
	yastronomy=dom.getElementsByTagNameNS(wser,'astronomy')[0]
	return {
		'current_condition': ycondition.getAttribute('text'),
		'current_temp': ycondition.getAttribute('temp'),
		'current_code': ycondition.getAttribute('code'),
		'forecasts': forecasts ,
    'humidity': yatmosphere.getAttribute('humidity'),
    'pressure': yatmosphere.getAttribute('pressure'),
    'rising': yatmosphere.getAttribute('rising'),
    'winddirection': ywind.getAttribute('direction'),
    'windspeed': ywind.getAttribute('speed'),
    'windchill': ywind.getAttribute('chill'),
    'sunrise': yastronomy.getAttribute('sunrise'),
    'sunset': yastronomy.getAttribute('sunset'),
	}


def downloadAndWriteWeather(woeid):
	seconds=int(datetime.now().strftime("%s"))
	currenttime=datetime.now().strftime("%I:%M %p")

	currentdate=datetime.now().strftime("%A %m/%d/%Y")

	try:
		weather=getWeather(woeid)
	except:
		e=sys.exc_info()[0]
		print "Error: %s" % e
		syslog.syslog(syslog.LOG_ERR,"Error: %s" % e)

	current_condition=weather['current_condition']
	current_temp=weather['current_temp']
	current_code=weather['current_code']
	humidity=weather['humidity']
	pressure=weather['pressure']
	rising=weather['rising']
	winddirection=weather['winddirection']
	windspeed=weather['windspeed']
	windchill=weather['windchill']
	sunrise=weather['sunrise']
	sunset=weather['sunset']

	getIndoorTempCmd="/var/www/html/BERTHA/therm.py -q | grep CurrentTemp | sed 's/CurrentTemp //'";
	# IndoorTemp=subprocess.check_output('{}'.format(getIndoorTempCmd),shell=True)
	#IndoorTemp=subprocess.Popen(format(getIndoorTempCmd),shell=True)
	IndoorTemp="NA"

	getIndoorSettingCmd="/var/www/html/BERTHA/therm.py -q | grep CoolSetpoint | sed 's/CoolSetpoint //'"
	# IndoorSetting=subprocess.check_output('{}'.format(getIndoorSettingCmd),shell=True)
	#IndoorSetting=subprocess.Popen(format(getIndoorSettingCmd),shell=True)
	IndoorSetting="NA"

	day0date=weather['forecasts'][0]['date']
	day0day=weather['forecasts'][0]['day']
	day0high=weather['forecasts'][0]['high']
	day0low=weather['forecasts'][0]['low']
	day0code=weather['forecasts'][0]['code']
	day0condition=weather['forecasts'][0]['condition']
	day1date=weather['forecasts'][1]['date']
	day1day=weather['forecasts'][1]['day']
	day1high=weather['forecasts'][1]['high']
	day1low=weather['forecasts'][1]['low']
	day1code=weather['forecasts'][1]['code']
	day1condition=weather['forecasts'][1]['condition']
	day2date=weather['forecasts'][2]['date']
	day2day=weather['forecasts'][2]['day']
	day2high=weather['forecasts'][2]['high']
	day2low=weather['forecasts'][2]['low']
	day2code=weather['forecasts'][2]['code']
	day2condition=weather['forecasts'][2]['condition']
	day3date=weather['forecasts'][3]['date']
	day3day=weather['forecasts'][3]['day']
	day3high=weather['forecasts'][3]['high']
	day3low=weather['forecasts'][3]['low']
	day3code=weather['forecasts'][3]['code']
	day3condition=weather['forecasts'][3]['condition']
	day4date=weather['forecasts'][4]['date']
	day4day=weather['forecasts'][4]['day']
	day4high=weather['forecasts'][4]['high']
	day4low=weather['forecasts'][4]['low']
	day4code=weather['forecasts'][4]['code']
	day4condition=weather['forecasts'][4]['condition']

	doc=Document()
	data=doc.createElement('data')
	doc.appendChild(data)

	now=doc.createElement('now')
	now.setAttribute("date",currentdate)
	now.setAttribute("time",currenttime)
	data.appendChild(now)

	astral=doc.createElement('astral')
	astral.setAttribute("sunrise",sunrise)
	astral.setAttribute("sunset",sunset)

	pos=position()
	moonphasename=phase(pos)
	moonphasenum=phasenum(pos)

	astral.setAttribute("moonphase",moonphasename)
	astral.setAttribute("moonphasenum",moonphasenum)
	data.appendChild(astral)

	weather=doc.createElement('weather')
	data.appendChild(weather)
	current=doc.createElement('current')
	weather.appendChild(current)
	current.setAttribute("temp",current_temp)
	current.setAttribute("humidity",humidity)
	current.setAttribute("pressure",pressure)
	current.setAttribute("rising",rising)
	current.setAttribute("winddirection",winddirection)
	current.setAttribute("windspeed",windspeed)
	current.setAttribute("windchill",windchill)
	current.setAttribute("condition",current_condition)
	current.setAttribute("code",current_code)
	current.setAttribute("indoor",IndoorTemp)
	current.setAttribute("setting",IndoorSetting)
	today=doc.createElement('today')
	today.setAttribute("high",day0high)
	today.setAttribute("low",day0low)
	forecast=doc.createElement('forecast')
	weather.appendChild(forecast)
	day0=doc.createElement('day0')
	day0.setAttribute("date",day0date)
	day0.setAttribute("day",day0day)
	day0.setAttribute("high",day0high)
	day0.setAttribute("low",day0low)
	day0.setAttribute("code",day0code)
	day0.setAttribute("precip",'100')
	day0.setAttribute("condition",day0condition)
	day1=doc.createElement('day1')
	day1.setAttribute("date",day1date)
	day1.setAttribute("day",day1day)
	day1.setAttribute("high",day1high)
	day1.setAttribute("low",day1low)
	day1.setAttribute("code",day1code)
	day1.setAttribute("precip",'100')
	day1.setAttribute("condition",day1condition)
	day2=doc.createElement('day2')
	day2.setAttribute("date",day2date)
	day2.setAttribute("day",day2day)
	day2.setAttribute("high",day2high)
	day2.setAttribute("low",day2low)
	day2.setAttribute("code",day2code)
	day2.setAttribute("precip",'100')
	day2.setAttribute("condition",day2condition)
	day3=doc.createElement('day3')
	day3.setAttribute("date",day3date)
	day3.setAttribute("day",day3day)
	day3.setAttribute("high",day3high)
	day3.setAttribute("low",day3low)
	day3.setAttribute("code",day3code)
	day3.setAttribute("precip",'100')
	day3.setAttribute("condition",day3condition)
	day4=doc.createElement('day4')
	day4.setAttribute("date",day4date)
	day4.setAttribute("day",day4day)
	day4.setAttribute("high",day4high)
	day4.setAttribute("low",day4low)
	day4.setAttribute("code",day4code)
	day4.setAttribute("precip",'100')
	day4.setAttribute("condition",day4condition)
	forecast.appendChild(day0)
	forecast.appendChild(day1)
	forecast.appendChild(day2)
	forecast.appendChild(day3)
	forecast.appendChild(day4)
	data.appendChild(weather)

	# doc.writexml(open("/usr/local/HyperClock/AstralData.txt","wb"),indent="  ",addindent="  ",newl='\n')
	doc.writexml(open(HyperConfig.cfg_AstralDataFile,"wb"),indent="  ",addindent="  ",newl='\n')

	doc.unlink()

