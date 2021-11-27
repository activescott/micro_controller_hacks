#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd)

source "$THISDIR/.env"

docker container rm "$MPY_CONTAINER_NAME"
