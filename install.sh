#!/bin/sh
##################################################################
# hyper_clock 4.0 by level6
# https://github.com/lleevveell66/HyperClock
##################################################################
# Find complete instructions on the HyperClock page.
##################################################################

echo "Installing HyperClock:"
echo " - Changing file modes of executables"
/bin/chmod 755 hyper_clock
/bin/chmod 755 scripts/get_indoor_temp.sh
/bin/chmod 755 scripts/get_weather.sh
echo " - Removing any previous directory /usr/local/HyperClock/"
/usr/bin/rm -r /usr/local/HyperClock/
echo " - Making the /usr/local/HyperClock/ directory"
/bin/mkdir -p /usr/local/HyperClock/

echo " - Copying everything here into /usr/local/HyperClock/"
/usr//bin/cp -a . /usr/local/HyperClock/

echo " - Installing required packages"
apt -y install python3-pygame
apt -y install python3-setuptools
apt -y install python3-skyfield
pip3 install --break-system-packages configparser

echo "Done!"
echo ""
echo "  Remember to edit /usr/local/HyperClock/conf/hyper_clock.conf to customize your HyperClock."
echo ""
echo ""
echo "  Remember to edit /usr/local/etc/api_keys.conf to customize your API key for OWM, if you are using that."
echo ""
echo "  To run it:  /usr/local/HyperClock/hyper_clock"
echo ""
echo "  See the following webpage for other instructions (making it run upon boot on an RPI, etc.):"
echo "    https://github.com/lleevveell66/HyperClock"
echo ""

exit 0

