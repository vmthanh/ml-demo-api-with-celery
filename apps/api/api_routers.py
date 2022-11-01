import os
import json
from typing import Dict

from loguru import logger
from fastapi import Request, APIRouter

import config
from core.schemas.trip import TripAPIRequestMessage, TripAPIResponseMessage
from core.schemas.health import Health
from core.services.trip_duration_api import TripDurationApi

API_VERSION = config.API_VERSION
MODEL_VERSION = config.MODEL_VERSION

api_router = APIRouter()


@api_router.get("/health", response_model=Health, status_code=200)
def health() -> Dict:
    return Health(
        name=config.PROJECT_NAME, api_version=API_VERSION, model_version=MODEL_VERSION
    ).dict()


@api_router.post(
    f"/{config.API_VERSION}/trip/predict",
    tags=["Trips"],
    response_model=TripAPIResponseMessage,
    status_code=200,
)
def trip_predict(request: Request, trip_request: TripAPIRequestMessage):
    api_service = TripDurationApi()
    results = api_service.process_raw_request(request, trip_request)
    return results
