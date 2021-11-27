#!/usr/bin/env sh
THISDIR=$(cd $(dirname "$0"); pwd)

source "$THISDIR/.env"

FALSE=1
TRUE=0

if [ $(docker container ls --filter "name=$MPY_CONTAINER_NAME" -a | wc -l) -eq 2 ]; then
  IS_CONTAINER_EXISTS=$TRUE
else
  IS_CONTAINER_EXISTS=$FALSE
fi

if [ $(docker container ls --filter "name=$MPY_CONTAINER_NAME" --filter "status=running" | wc -l) -eq 2 ]; then
  IS_CONTAINER_RUNNING=$TRUE
else
  IS_CONTAINER_RUNNING=$FALSE
fi

echo "IS_CONTAINER_EXISTS: $IS_CONTAINER_EXISTS"
echo "IS_CONTAINER_RUNNING: $IS_CONTAINER_RUNNING"

if [ $IS_CONTAINER_RUNNING -eq $TRUE ]; then
  echo "Container \"$MPY_CONTAINER_NAME\" is running."
else
  if [ $IS_CONTAINER_EXISTS -eq $TRUE ]; then
    echo "Removing existing $MPY_CONTAINER_NAME container before starting a fresh one..."
    docker container rm $MPY_CONTAINER_NAME  
  fi

  echo "Starting container $MPY_CONTAINER_NAME..."
  docker run \
    --detach \
    --tty \
    --name "$MPY_CONTAINER_NAME" \
    micropython-unix:latest

  EXIT_CODE=$?
  [[ $EXIT_CODE -eq 0 ]] || die "Failed to start container! Docker returned exit code \"$EXIT_CODE\""
fi
