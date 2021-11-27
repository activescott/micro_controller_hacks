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
USAGE: $THISSCRIPT <PATH> | <PACKAGE_NAME>

Installs a package onto the device from a local directory (PATH) or a PyPI (PACKAGE_NAME).

Examples:
  Install from local package source directory:
    ./install-package.sh ../../drivers/micropython-motor-driver-dual-tb6612fng/

  Install using PyPi package name:
    ./install-package.sh micropython-rfsocket

END_DOC

}

# Basically we install the package on the device with these steps:
# 1. Install w/ pip into a local temp directory (to unbundle it and get the python modules extracted).
# 2. Copy the intalled package dir onto device using mpremote

PACKAGE_NAME_OR_PATH=$1

##### Create temp dir #####
PKG_DIR=$THISDIR/intalled_packages
mkdir "$PKG_DIR"

##### install w/ pip #####
#python3 -m pip install --target "$PKG_DIR" "$PACKAGE_NAME_OR_PATH"

TMPF=$THISDIR/temppipout
echo "TMPF: $TMPF"
python3 -m pip install --target "$PKG_DIR" "$PACKAGE_NAME_OR_PATH" 
echo "pip installed '$PACKAGE_NAME_OR_PATH' at '$PKG_DIR'."

##### copy to device #####
echo "Creating /lib dir on device (this may error if it already exists)..."
./fs.sh mkdir /lib

echo "Copying packages to device:"
for f in $PKG_DIR/*.py
do
  # remote copy only copies full path name of host mpremote connect $MP_DEVICE fs cp "$PKG_DIR" ":"
  echo "copying $(basename $f) to /lib/"
  mpremote connect $MP_DEVICE fs cp "$f" ":/lib/$(basename $f)"
done

##### cleanup #####

