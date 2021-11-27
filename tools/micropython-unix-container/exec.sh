#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd)

source "$THISDIR/.env"

docker exec \
  -it \
  --workdir "/usr/src/micropython/ports/unix" \
  "$MPY_CONTAINER_NAME" \
  "$@"
