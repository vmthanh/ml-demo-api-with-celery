#!/usr/bin/env sh

USERNAME="$(id -u -n)"
MODULE="apps.api"
SOCKET="0.0.0.0:8182"
MODULE_APP="${MODULE}.main:app"
CONFIG_PATH="boot/uvicorn/config.py"
REPO_ROOT="repo"
LOGS_ROOT="${REPO_ROOT}/logs/apps/api"
LOGS_PATH="${LOGS_ROOT}/daemon.log"

sudo mkdir -p ${LOGS_ROOT} && \
sudo chown -R ${USERNAME} ${LOGS_ROOT} && \
sudo chown -R ${USERNAME} ${REPO_ROOT} && \

gunicorn \
    --name "${MODULE}" \
    --config "${CONFIG_PATH}" \
    --bind "${SOCKET}" \
    --log-file "${LOGS_PATH}" \
    "${MODULE_APP}"
