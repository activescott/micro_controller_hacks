#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
source "$THISDIR/.env"

# This prevents main.py from being on the device which can brick it
#$THISDIR/deploy-to-device.sh
#mpremote connect $MP_DEVICE "run" "main.py"

"$THISDIR/deploy-dependencies.sh"

mpremote connect $MP_DEVICE  mount . exec "import test_pulse_freq"
