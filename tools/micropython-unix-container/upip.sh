#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd)

source "$THISDIR/.env"

#docker run \
#  -it \
#  --workdir "/usr/src/micropython/ports/unix" \
#  --name "$MPY_CONTAINER_NAME" \
#  micropython-unix:latest \
#  "micropython" -m upip "$@"

docker run \
  -it \
  --workdir "/usr/src/micropython/ports/unix" \
  micropython-unix:latest \
  "micropython" -m upip "$@"
