#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
source "$THISDIR/.env"
"$THISDIR/deploy-dependencies.sh"

# NOTE: Using mount rather than a full deploy prevents main.py from being on the device which can brick it

CMD=main.py
if [ "$#" -ge 1 ]; then
  CMD=$1
fi
mpremote connect $MP_DEVICE  mount . run $CMD
