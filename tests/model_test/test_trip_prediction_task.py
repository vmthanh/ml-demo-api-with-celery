from core.utilities.cls_constants import APIReply
from core.services.trip_duration_prediction_task import (
    TripDurationTask,
    preprare_feature,
)


def test_trip_duration_task_process_func():
    # Given
    pu_location_id: int = 130
    do_location_id: int = 205
    trip_distance: float = 3
    # When
    result = TripDurationTask().process(pu_location_id, do_location_id, trip_distance)
    # Then
    assert result["reply_code"] == APIReply.SUCCESS
    assert result["duration"] == 12.785509620119132


def test_trip_duration_task_prepare_feature():
    # Given
    pu_location: int = 130
    do_location: int = 205
    trip_distance: float = 3
    # When
    features = preprare_feature(pu_location, do_location, trip_distance)
    # Then
    expected_features = {"PU_DO": "130_205", "trip_distance": 3}
    assert features["PU_DO"] == expected_features["PU_DO"]
    assert features["trip_distance"] == expected_features["trip_distance"]
