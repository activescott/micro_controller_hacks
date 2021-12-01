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

Installs this app and all the necessary libs onto the device

END_DOC

}

"$THISDIR/deploy-dependencies.sh"

echo "\nCopying app code to device:"
for f in $THISDIR/*.py
do
  # remote copy only copies full path name of host mpremote connect $MP_DEVICE fs cp "$PKG_DIR" ":"
  #echo "copying $(basename $f) to /:"
  mpremote connect $MP_DEVICE fs cp "$f" ":/$(basename $f)"
done

echo ""
echo "listing files on device:"
mpremote connect $MP_DEVICE ls /
