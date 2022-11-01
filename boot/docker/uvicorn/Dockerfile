
ARG VM_BASE
FROM $VM_BASE

ARG VM_USER
ARG VM_HOME
ARG VM_CODE
ARG VM_PIP

COPY . $VM_CODE
WORKDIR $VM_CODE/
RUN rm -rf libs
RUN apk add --no-cache sudo \
    && apk add --no-cache --virtual .build-deps gcc musl-dev g++\
    && pip install --no-cache-dir -r $VM_PIP \
    && apk del .build-deps

RUN apk add --no-cache bash

RUN adduser --disabled-password --gecos '' $VM_USER \
    && addgroup sudo \
    && adduser $VM_USER sudo \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && chown -R $VM_USER $VM_HOME

USER $VM_USER

WORKDIR $VM_CODE/
EXPOSE 8182
ENTRYPOINT ["boot/docker/uvicorn/entrypoint.sh"]
