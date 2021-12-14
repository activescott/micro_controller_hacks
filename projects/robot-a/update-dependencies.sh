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

Updates the dependencies of this app in the local /lib folder (which is copied to the device during deploy)

END_DOC

}

echo "\nCreating local /lib dir"
LIBDIR="$THISDIR/lib"
[ -d $LIBDIR ] && rm -rf $LIBDIR
mkdir $LIBDIR

echo "\nCopying packages to local /lib dir:"
cp -v ../../drivers/micropython-motor-driver-dual-tb6612fng/tb6612fng.py "$LIBDIR/"
cp -v ../../drivers/micropython-hcsr04/hcsr04.py "$LIBDIR/"
cp -v ../../drivers/micropython-open-lcd-driver/open_lcd.py "$LIBDIR/"
cp -v ../../drivers/micropython-qmc5883l-magnetic-compass-sensor-driver/qmc5883l.py "$LIBDIR/"
cp -v ../../drivers/micropython-wheel-encoder-hall-effect-sensor/encoder.py "$LIBDIR/"
cp -v ../../drivers/micropython-wheel-encoder-hall-effect-sensor/funcs.py "$LIBDIR/"
