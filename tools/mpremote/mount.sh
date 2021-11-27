#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory

source $THISDIR/.env

echo "Running mount (after the directory is mounted run `import yourscript`" to run it
mpremote connect $MP_DEVICE mount $1
