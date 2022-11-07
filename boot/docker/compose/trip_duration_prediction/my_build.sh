#!/usr/bin/env bash
COMMIT_ID=$(git rev-parse HEAD || echo "latest")
DOCKER_IMAGE_PROJECT_ROOT_NAME="trip_duration_prediction"
export COMMIT_ID=${COMMIT_ID}
export DOCKER_IMAGE_PROJECT_ROOT_NAME=${DOCKER_IMAGE_PROJECT_ROOT_NAME}

PROJECT_ROOT="${PWD}"
DC_ROOT="${PROJECT_ROOT}/boot/docker/compose/trip_duration_prediction"

export HOST_REPO_DIR="${PROJECT_ROOT}/repo"

CMD="$@"
DC_FILES="\
    -f ${DC_ROOT}/docker-compose.yml \
    -f ${DC_ROOT}/docker-compose.dev.yml \
    -f ${DC_ROOT}/docker-compose.cpu.yml"
DC_ENV_FILE="${DC_ROOT}/.env"
source "${DC_ROOT}/docker-services.sh" \
  "${CMD}" \
  "${DC_FILES}" \
  "${DC_ENV_FILE}" \


if [[ "${CMD}" == "up" ]]
then
    docker-compose ${DC_FILES} up -d --no-build --no-recreate redis
    docker-compose ${DC_FILES} up -d --no-build --no-deps --scale worker_0=1 worker_0
    docker-compose ${DC_FILES} up -d --no-build --no-deps web
fi

if [[ "${CMD}" == "logs" ]]
then
    docker-compose ${DC_FILES} logs -f
fi
