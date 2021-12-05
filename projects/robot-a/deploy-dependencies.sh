#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
THISSCRIPT=$(basename $0)

source $THISDIR/.env

die () {
    echo >&2 "$@"
    help
    exit 1
}

help () {
  echo 
  cat << END_DOC
USAGE: $THISSCRIPT

Installs this app's libs onto the device

END_DOC

}

"$THISDIR/update-dependencies.sh"

echo "\nCreating /lib dir on device (this may error if it already exists)..."
mpremote connect $MP_DEVICE fs mkdir /lib

echo "\nCopying packages to device:"
for f in $THISDIR/lib/*.py
do
  # remote copy only copies full path name of host mpremote connect $MP_DEVICE fs cp "$PKG_DIR" ":"
  #echo "copying $(basename $f) to /lib/"
  mpremote connect $MP_DEVICE fs cp "$f" ":/lib/$(basename $f)"
done
