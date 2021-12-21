#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
PARENTDIR=$(dirname $THISDIR)

source "$THISDIR/.env"

# copy dependencies:
echo "\nCopying packages to local /lib dir:"
mpremote connect $MP_DEVICE fs mkdir /lib
for DRIVER_FILE in encoder.py
do
  mpremote connect $MP_DEVICE fs rm "/lib/$DRIVER_FILE"
  mpremote connect $MP_DEVICE fs cp "$PARENTDIR/$DRIVER_FILE" ":/lib/$DRIVER_FILE"
done

# we need the motor driver for some examples:
mpremote connect $MP_DEVICE fs cp "../../../drivers/micropython-motor-driver-dual-tb6612fng/tb6612fng.py" ":/lib/"

CMD=rotate_n_times.py
if [ "$#" -ge 1 ]; then
  CMD=$1
fi
mpremote connect $MP_DEVICE mount . run $CMD
