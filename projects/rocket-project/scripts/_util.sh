#!/bin/bash
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
THISSCRIPT=$(basename $0)
PROJECT_DIR=$(cd "$THISDIR/.."; pwd)
SOURCE_DIR=$(cd "$PROJECT_DIR/src"; pwd)

source $PROJECT_DIR/.env

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

# Validate some assumptions about our environment:
#[ -z "$MP_DEVICE" ] && die "MP_DEVICE environment variable not set. You can set it in '$PROJECT_DIR/.env'"
[ -d "$SOURCE_DIR" ] || die "Source directory '$SOURCE_DIR' does not exist"

echo "Using device /dev/cu.usbserial-1420..."