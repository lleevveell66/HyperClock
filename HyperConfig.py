#!/usr/bin/env python
##########################################################
# HyperConfig v3.0 by level6
# https://github.com/lleevveell66/HyperClock
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Read in HyperClock configuration information from HyperClock.conf
##########################################################

import os, pygame, time, datetime, random, sys, urllib, ConfigParser, syslog

config=ConfigParser.ConfigParser()

try:
	config.readfp(open(r'/usr/local/HyperClock/HyperClock.conf'))
except:
	e=sys.exc_info()[0]
	print "HyperClock.conf Parsing Error: %s" % e
	print "/usr/local/HyperClock/HyperClock.conf exists?"
	syslog.syslog(syslog.LOG_ERR,"HyperClock.conf Parsing Error: %s" % e)
	syslog.syslog(syslog.LOG_ERR,"/usr/local/HyperClock/HyperClock.conf exists?")
	print "Exiting."
	syslog.syslog(syslog.LOG_ERR,"Exiting.")
	sys.exit();

cfg_Topology=config.get('HyperClock','topology')
cfg_AstralDataFile=config.get('HyperClock','AstralDataFile')
cfg_AstralDataCommand=config.get('HyperClock','AstralDataCommand')
cfg_IndoorTempFile=config.get('HyperClock','IndoorTempFile')
cfg_IndoorTempCommand=config.get('HyperClock','IndoorTempCommand')
cfg_woeid=config.get('HyperClock','woeid')
cfg_timefont=config.get('HyperClock','timefont')
cfg_datefont=config.get('HyperClock','datefont')
cfg_weatherfont=config.get('HyperClock','weatherfont')
cfg_tempfont=config.get('HyperClock','tempfont')
cfg_itempfont=config.get('HyperClock','itempfont')
cfg_highfont=config.get('HyperClock','highfont')
cfg_lowfont=config.get('HyperClock','lowfont')
cfg_forecastfont=config.get('HyperClock','forecastfont')
cfg_windfont=config.get('HyperClock','windfont')
cfg_pressurefont=config.get('HyperClock','pressurefont')
cfg_humidityfont=config.get('HyperClock','humidityfont')
cfg_sunrisesetfont=config.get('HyperClock','sunrisesetfont')
cfg_lastfont=config.get('HyperClock','lastfont')
cfg_timecolor=config.get('HyperClock','timecolor')
cfg_datecolor=config.get('HyperClock','datecolor')
cfg_weathercolor=config.get('HyperClock','weathercolor')
cfg_tempcolor=config.get('HyperClock','tempcolor')
cfg_itempcolor=config.get('HyperClock','itempcolor')
cfg_highcolor=config.get('HyperClock','highcolor')
cfg_lowcolor=config.get('HyperClock','lowcolor')
cfg_windcolor=config.get('HyperClock','windcolor')
cfg_pressurecolor=config.get('HyperClock','pressurecolor')
cfg_humiditycolor=config.get('HyperClock','humiditycolor')
cfg_day1color=config.get('HyperClock','day1color')
cfg_day2color=config.get('HyperClock','day2color')
cfg_day3color=config.get('HyperClock','day3color')
cfg_day4color=config.get('HyperClock','day4color')
cfg_sunrisecolor=config.get('HyperClock','sunrisecolor')
cfg_sunsetcolor=config.get('HyperClock','sunsetcolor')
cfg_lastcolor=config.get('HyperClock','lastcolor')


