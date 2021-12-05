#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
PARENTDIR=$(dirname $THISDIR)

source "$THISDIR/.env"


# copy dependencies:
DRIVER_FILE=qmc5883l.py

LIBDIR="$THISDIR"
echo "\nCopying packages to local /lib dir:"
cp -v ../../drivers/micropython-open-lcd-driver/open_lcd.py "$LIBDIR/"
cp -v ../../drivers/micropython-qmc5883l-magnetic-compass-sensor-driver/qmc5883l.py "$LIBDIR/"

CMD=test.py
if [ "$#" -ge 1 ]; then
  CMD=$1
fi
mpremote connect $MP_DEVICE  mount . run $CMD
