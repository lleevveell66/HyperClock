#!/bin/sh

# Use this for a WiFi Honeywell thermostat via My Total Connect
#USERNAME=CHANGEME@CHANGEME.CH
#PASSWORD=CHANGEME
#DEVICEID=CHANGME
#extras/therm.py -U $USERNAME -P $PASSWORD -D $DEVICEID -q | grep ^CurrentTemp|cut -d\  -f2|sed 's/\..*//'>/usr/local/HyperClock/CurrentIndoorTemp

# Use this for a DS18B20 type of probe
# (https://www.amazon.com/gp/product/B00Q9YBIJI/ref=oh_aui_detailpage_o06_s01?ie=UTF8&psc=1)
/usr/local/HyperClock/extras/IndoorTemp > /usr/local/HyperClock/CurrentIndoorTemp

# Dummy to show no indoor temperature
#echo "9999" > /usr/local/HyperClock/CurrentIndoorTemp
