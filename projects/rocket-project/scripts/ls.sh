#!/bin/bash
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory

source "$THISDIR/_util.sh"

echo "listing files on device:"
# NOTE: We're letting the mpremote find and select the device. This is probably fine with only a single device plugged in.

mpremote ls /
