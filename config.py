import os
import json
import time

PROJECT_NAME = "TRIP DURATION MODEL PREDICTION API"
PROJECT_APP = os.environ.get("PROJECT_APP", "apps.api")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
API_VERSION = os.environ.get("API_VERSION", "v1")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "1.0.0")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_LOGS_DIR = os.path.join(PROJECT_DIR, "repo", "logs")


class ModelConfig:

    CONFIG_JSON = "repo/config.json"
    CONFIG_DICT = {
        "TRIP_DURATION_MODEL": "repo/models/lin_reg.bin",
        "TRIP_DURATION_THRESHOLD": 0.3,
    }

    CACHE_TIMEOUT = 60
    CACHE_TIMESTAMP = None

    @classmethod
    def update(cls):
        now = time.time()
        timeout = cls.CACHE_TIMEOUT
        timestamp = cls.CACHE_TIMESTAMP
        if timestamp and abs(now - timestamp) < timeout:
            return
        cls.CACHE_TIMESTAMP = now
        config_path = cls.CONFIG_JSON
        if not (
            os.path.isfile(config_path)
            and (not timestamp or os.path.getmtime(config_path) >= timestamp)
        ):
            return
        try:
            with open(config_path, encoding="utf-8") as f:
                config_dict = json.load(f)
            for key, value in config_dict.items():
                if key not in cls.CONFIG_DICT:
                    continue
                cls.CONFIG_DICT[key] = value
        except Exception as ex:  # pylint: disable=broad-except
            assert ex

    @classmethod
    def trip_duration_model(cls):
        cls.update()
        return cls.CONFIG_DICT["TRIP_DURATION_MODEL"]

    @classmethod
    def trip_duration_threshold(cls):
        cls.update()
        return cls.CONFIG_DICT["TRIP_DURATION_THRESHOLD"]


class RedisConfig:

    HOST = os.environ.get("REDIS_HOST", None)
    PORT = os.environ.get("REDIS_PORT", None)


class GpuMemoryConfig:
    GPU_MEGABYTE_SET = os.environ.get("GPU_MEMORY_SET", 3000)


class CeleryTasksGeneralConfig:
    task_trip_queue = "tasks.trip"
    task_trip_prefix = "tasks.trip.tasks"
    task_process_trip = f"{task_trip_prefix}.predict_ride"

    broker_url = os.environ.get("CELERY_BROKER_URL", None)
    result_backend = os.environ.get("CELERY_RESULT_BACKEND", None)
    worker_prefetch_multiplier = int(
        os.environ.get("CELERY_WORKER_PREFETCH_MULTIPLIER", 1)
    )
