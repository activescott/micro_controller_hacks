#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory

source $THISDIR/.env
mpremote connect $MP_DEVICE fs cat "$@"

