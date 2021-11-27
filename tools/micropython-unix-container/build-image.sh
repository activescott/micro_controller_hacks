#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd)

source "$THISDIR/.env"

docker build -t micropython-unix -f micropython-unix.containerfile "$THISDIR"
