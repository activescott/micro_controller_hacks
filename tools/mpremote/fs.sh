#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd) #this script's directory
THISSCRIPT=$(basename $0)

source $THISDIR/.env

help () {
  echo 
  cat << END_DOC
USAGE: $THISSCRIPT <command> <args...>

execute filesystem commands on the device

command may be: cat, ls, cp, rm, mkdir, rmdir
use ":" as a prefix to specify a file on the device

END_DOC
}

die () {
    echo >&2 "$@"
    help
    exit 1
}

[ "$#" -ge 1 ] || die "command required"
echo $1 | grep -E -q '^cat|ls|cp|rm|mkdir|rmdir$' || die "unexpected command ($1)"

mpremote connect $MP_DEVICE fs "$@"

