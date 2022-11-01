import os
import math
import uuid

import requests

import config
from core.schemas.trip import TripAPIResponseMessage
from core.schemas.health import Health


def test_health_endpoint():
    # Given
    full_url = "http://localhost:8182/health"

    # When
    response = requests.get(full_url)
    # Then
    expected_result = Health(
        name=config.PROJECT_NAME,
        api_version=config.API_VERSION,
        model_version=config.MODEL_VERSION,
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == expected_result.dict()


def test_trip_predict():
    # Given
    full_url = "http://localhost:8182/v1/trip/predict"

    payload = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3,
        "request_id": str(uuid.uuid4()),
    }
    response = requests.post(url=full_url, json=payload)
    # Then
    expected_result = TripAPIResponseMessage(reply_code=0, duration=12.785509620119132)
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["reply_code"] == 0
    assert math.isclose(
        prediction_data["duration"], expected_result.duration, rel_tol=1e-3
    )


def test_trip_predict_missing_field():
    # Given
    full_url = "http://localhost:8182/v1/trip/predict"
    payload = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3,
    }  # Miss request_id field
    response = requests.post(url=full_url, json=payload)
    # Then
    assert response.status_code == 400
