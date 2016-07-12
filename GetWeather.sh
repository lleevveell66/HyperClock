#!/bin/sh

wget -q -N http://192.168.44.55/BERTHA/HyperClock/AstralData.txt -O /usr/local/HyperClock/AstralDataNew.txt
data=`cat /usr/local/HyperClock/AstralDataNew.txt | grep forecast`
if [ -z "$data" ]; then
 exit
else
 /bin/cp /usr/local/HyperClock/AstralDataNew.txt /usr/local/HyperClock/AstralData.txt
fi

exit 0

