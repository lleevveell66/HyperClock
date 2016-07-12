#!/bin/sh
##################################################################
# HyperClock 2.0 by level6 of LIE
##################################################################
# http://www.awja.org:8090/display/~level6/HyperClock
# Find complete instructions on the HyperClock page.
##################################################################

echo "Installing HyperClock ..."
/bin/chmod 755 HyperClock
/bin/chmod 755 GetIndoorTemp.sh
/bin/chmod 755 GetWeather.sh
/bin/mkdir -p /usr/local/HyperClock/

/bin/cp -a . /usr/local/HyperClock/

echo "Done!"
echo "  Remember to edit /usr/local/HyperClock/HyperClock.conf to customize your HyperClock"
echo "  To run it:  /usr/local/HyperClock/HyperClock"
echo "  See the webpage for other instructions (making it run upon boot on an RPI, etc.):"
echo "    http://www.awja.org:8090/display/~level6/HyperClock"

exit 0

