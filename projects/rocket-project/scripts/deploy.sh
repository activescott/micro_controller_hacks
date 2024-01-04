#!/bin/bash
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory

source "$THISDIR/_util.sh"

echo "Copying app code to device:"
for f in $SOURCE_DIR/*.py
do
  # remote copy only copies full path name of host mpremote connect $MP_DEVICE fs cp "$PKG_DIR" ":"
  #echo "copying $(basename $f) to /:"
  mpremote fs cp "$f" ":/$(basename $f)"
done

echo ""
echo "The files on the device now are:"
mpremote ls /
