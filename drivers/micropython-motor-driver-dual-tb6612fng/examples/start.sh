#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
source "$THISDIR/.env"

PARENTDIR=$(dirname $THISDIR)

mpremote connect $MP_DEVICE fs mkdir /lib
mpremote connect $MP_DEVICE fs rm /lib/tb6612fng.py
mpremote connect $MP_DEVICE fs cp "$PARENTDIR/tb6612fng.py" ":/lib/tb6612fng.py"

mpremote connect $MP_DEVICE  mount . exec "import simple"
