#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
source "$THISDIR/.env"
"$THISDIR/deploy-dependencies.sh"

CMD=simple.py
if [ "$#" -ge 1 ]; then
  CMD=$1
fi
mpremote connect $MP_DEVICE  mount . run $CMD
