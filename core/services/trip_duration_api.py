import collections

import celery
from loguru import logger
from fastapi import Request
from fastapi.encoders import jsonable_encoder

import config
from core.schemas.trip import TripAPIRequestMessage, TripAPIResponseMessage
from core.utilities.cls_time import Timer

task_celery = config.CeleryTasksGeneralConfig
celery_app = celery.Celery()
celery_app.config_from_object(task_celery)


class TripDurationApi:
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.fastapi_raw_request = None

        self.trip_request = None
        self.response = None
        self.results = None
        self.status_code = None
        self.timer = None
        self.timings = None

    def call_celery_matching(
        self,
        pu_location_id: int,
        do_location_id: int,
        trip_distance: float,
    ):
        """
        :type celery_result: celery.result.AsyncResult
        """
        celery_result = celery_app.send_task(
            task_celery.task_process_trip,
            args=[
                pu_location_id,
                do_location_id,
                trip_distance,
            ],
            queue=task_celery.task_trip_queue,
        )

        return celery_result

    def process_api_request(self):
        celery_result = self.call_celery_matching(
            self.trip_request.PULocationID,
            self.trip_request.DOLocationID,
            self.trip_request.trip_distance,
        )

        results: dict = {}
        try:
            results = celery_result.get(timeout=60)
            celery_result.forget()
            results = results or {}
        except celery.exceptions.TimeoutError:
            results = {}

        reply_code: int = results.pop("reply_code", 1)
        duration: float = float(results.pop("duration", 0.0))

        self.response = TripAPIResponseMessage(reply_code=reply_code, duration=duration)
        self.status_code = 200
        self.timings = results.pop("timings", {})
        self.results = results

    def log_request_dict(self):
        request_info = self.trip_request.dict()
        return collections.OrderedDict(
            [
                ("uri", self.fastapi_raw_request.url.path),
                ("method", self.fastapi_raw_request.method),
                ("ip", self.fastapi_raw_request.client.host),
                ("elapsed", self.timer.since_ms if self.timer is not None else 0),
                ("request", request_info),
            ]
        )

    def log_response_dict(self):
        log_dict = self.log_request_dict()
        log_dict.update(
            collections.OrderedDict(
                [
                    (
                        "response",
                        self.response.dict() if self.response is not None else None,
                    ),
                    (
                        "status_code",
                        self.status_code if self.status_code is not None else 0,
                    ),
                    ("result", self.results),
                    ("timings", self.timings),
                ]
            )
        )
        return log_dict

    # @exception_safe
    def log_response(self):
        log_dict = self.log_response_dict()
        log_params = jsonable_encoder(log_dict)
        log_type = "response"
        logger.info(f"{log_type}|{log_params}")

    def process_raw_request(
        self, raw_request: Request, trip_request: TripAPIRequestMessage
    ):
        self.timer = Timer()
        self.fastapi_raw_request = raw_request
        self.trip_request = trip_request
        with self.timer:
            try:
                self.process_api_request()
            finally:
                self.log_response()
            return self.response
