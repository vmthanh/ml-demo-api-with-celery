#!/usr/bin/env bash
CMD="$1"
DC_FILES="$2"
DC_ENV_FILE="$3"
cp -p "${DC_ENV_FILE}" .env

WORKERS="worker worker_0 worker_1 worker_2 worker_3"


if [[ "${CMD}" == "push" ]];                then docker-compose ${DC_FILES} push;                                   fi
if [[ "${CMD}" == "pull" ]];                then docker-compose ${DC_FILES} pull;                                   fi

if [[ "${CMD}" == "build" ]];               then docker-compose ${DC_FILES} build web worker;                 fi
if [[ "${CMD}" == "build web" ]];           then docker-compose ${DC_FILES} build web;                              fi
if [[ "${CMD}" == "build worker" ]];        then docker-compose ${DC_FILES} build worker;                           fi

if [[ "${CMD}" == "restart" ]];             then docker-compose ${DC_FILES} restart web ${WORKERS};         fi
if [[ "${CMD}" == "restart web" ]];         then docker-compose ${DC_FILES} restart web;                    fi
if [[ "${CMD}" == "restart worker" ]];      then docker-compose ${DC_FILES} restart ${WORKERS};             fi
if [[ "${CMD}" == "restart redis" ]];       then docker-compose ${DC_FILES} restart redis;                  fi

if [[ "${CMD}" == "stop" ]];                then docker-compose ${DC_FILES} stop web ${WORKERS};            fi
if [[ "${CMD}" == "stop web" ]];            then docker-compose ${DC_FILES} stop web;                       fi
if [[ "${CMD}" == "stop worker" ]];         then docker-compose ${DC_FILES} stop ${WORKERS};                fi
if [[ "${CMD}" == "stop redis" ]];          then docker-compose ${DC_FILES} stop redis;                     fi

if [[ "${CMD}" == "rm" ]];                  then docker-compose ${DC_FILES} rm web ${WORKERS};              fi
if [[ "${CMD}" == "rm web" ]];              then docker-compose ${DC_FILES} rm web;                         fi
if [[ "${CMD}" == "rm worker" ]];           then docker-compose ${DC_FILES} rm ${WORKERS};                  fi
if [[ "${CMD}" == "kill" ]];                then docker-compose ${DC_FILES} down;                           fi

yes_or_no()
{
    read -p "$1 (Y/N) " -n 1 -r
    echo
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
}


if [[ "${CMD}" == "down" ]]
then
    echo
    yes_or_no "It will stop and remove everything, including the Redis server. Are you sure?"
    sleep 1
    yes_or_no "Redis keeps the embedding data. Have you informed the person in charge?"

    docker-compose ${DC_FILES} down
fi
