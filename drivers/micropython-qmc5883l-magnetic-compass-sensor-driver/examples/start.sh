#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
PARENTDIR=$(dirname $THISDIR)

source "$THISDIR/.env"


# copy dependencies:
DRIVER_FILE=qmc5883l.py
mpremote connect $MP_DEVICE fs mkdir /lib
mpremote connect $MP_DEVICE fs rm "/lib/$DRIVER_FILE"
mpremote connect $MP_DEVICE fs cp "$PARENTDIR/$DRIVER_FILE" ":/lib/$DRIVER_FILE"

CMD=simple.py
if [ "$#" -ge 1 ]; then
  CMD=$1
fi
mpremote connect $MP_DEVICE  mount . run $CMD
