import celery

import config
from core.utilities.cls_loguru_config import loguru_setting
from core.services.trip_duration_prediction_task import TripDurationTask

loguru_setting.setup_app_logging()

app = celery.Celery()
app.config_from_object(config.CeleryTasksGeneralConfig)
app.autodiscover_tasks(["tasks.trip"])


@celery.shared_task(time_limit=60, soft_time_limit=60)
def predict_ride(pu_location_id: int, do_location_id: int, trip_distance: float):
    return TripDurationTask().process(pu_location_id, do_location_id, trip_distance)
