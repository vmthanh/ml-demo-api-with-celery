#!/usr/bin/env bash

USERNAME="$(id -u -n)"
MODULE="tasks.trip"
REPO_ROOT="repo"
LOGS_ROOT="${REPO_ROOT}/logs/tasks/trip"
LOGS_PATH="${LOGS_ROOT}/daemon.log"

sudo mkdir -p ${LOGS_ROOT} && \
sudo chown -R ${USERNAME} ${LOGS_ROOT} && \
sudo chown -R ${USERNAME} ${REPO_ROOT} && \
source activate venv && \
python -m celery worker \
    -A ${MODULE} \
    -Q ${MODULE} \
    -P threads \
    --prefetch-multiplier=1 \
    --concurrency=4 \
    --loglevel=INFO \
    --logfile="${LOGS_PATH}"
