import pickle
import collections

# import boto3
from loguru import logger

import config
from core.utilities.cls_time import DictKeyTimer
from core.utilities.cls_constants import APIReply

# s3 = boto3.resource("s3")

# TRIP_DURATION_MODEL_KEY = config.ModelConfig.s3_trip_model_key()
# TRIP_DURATION_MODEL_BUCKET = config.ModelConfig.s3_bucket()


TRIP_DURATION_MODEL_PATH = config.ModelConfig.trip_duration_model()
with open(TRIP_DURATION_MODEL_PATH, "rb") as f_in:
    dv, model = pickle.load(f_in)


def preprare_feature(pu_location_id: int, do_location_id: int, trip_distance: float):
    features = {}
    features["PU_DO"] = f"{pu_location_id}_{do_location_id}"
    features["trip_distance"] = trip_distance
    return features


class TripDurationTask:
    @classmethod
    def process(cls, pu_location_id: int, do_location_id: int, trip_distance: float):
        try:
            timings = collections.OrderedDict()
            step_name = "feature_prepare"
            with DictKeyTimer(timings, step_name):
                features = preprare_feature(
                    pu_location_id, do_location_id, trip_distance
                )
            step_name = "model_predict"
            with DictKeyTimer(timings, step_name):
                pred = cls.predict(features)
                logger.info(f"Predict duration:{pred}")

            result = {
                "duration": pred,
                "reply_code": APIReply.SUCCESS,
                "timings": timings,
            }
        # pylint: disable=broad-except
        except Exception:
            result = {
                "duration": 0.0,
                "reply_code": APIReply.ERROR_SERVER,
                "timings": timings,
            }
        return result

    @classmethod
    def predict(cls, features: dict):
        X = dv.transform(features)
        preds = model.predict(X)
        return float(preds[0])
