#!/bin/sh
##################################################################
# HyperClock 4.0 by level6
# https://github.com/lleevveell66/HyperClock
##################################################################
# Find complete instructions on the HyperClock page.
##################################################################

echo "Installing HyperClock:"
echo " - Changing file modes of executables"
/bin/chmod 755 HyperClock
/bin/chmod 755 scripts/get_indoor_temp.sh
/bin/chmod 755 scripts/get_weather.sh
echo " - Removing any previous directory /usr/local/HyperClock/"
\rm -r /usr/local/HyperClock/
echo " - Making the /usr/local/HyperClock/ directory"
/bin/mkdir -p /usr/local/HyperClock/

echo " - Copying everything here into /usr/local/HyperClock/"
/bin/cp -a . /usr/local/HyperClock/

echo "Done!"
echo ""
echo "  Remember to edit /usr/local/HyperClock/HyperClock.conf to customize your HyperClock."
echo ""
echo "  To run it:  /usr/local/HyperClock/HyperClock"
echo ""
echo "  See the following webpage for other instructions (making it run upon boot on an RPI, etc.):"
echo "    https://github.com/lleevveell66/HyperClock"

exit 0

