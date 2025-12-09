#!/bin/sh
#######################################################################
# GetWeather.sh v4.0 by level6 of LIE
#######################################################################


#######################################################################
# Uncomment this section to grab the data from a central server:
#######################################################################
#
# URL="http://my-weather-host.com/RemoteStagingDir/weather_data.json"
# # Stage the downloaded file into tmp/ dir:
# wget -q -N ${URL} -O /usr/local/HyperClock/tmp/weather_data.json
#
#######################################################################

# or...

#######################################################################
# Uncomment this section to use the OpenWeatherMap API to gather weather data, locally:
#######################################################################

/usr/local/HyperClock/owm_tools/get_owm_weather > /usr/local/HyperClock/tmp/weather_data_json

#######################################################################



# Check for an empty or corrupt file, or copy into place if good:
data=$(/usr/bin/cat /usr/local/HyperClock/tmp/weather_data.json | /usr/bin/grep weather)
if [ -z "$data" ]; then
  exit
else
  /usr/bin/cp /usr/local/HyperClock/tmp/weather_data.json /usr/local/HyperClock/data/weather_data.json
fi


exit 0

