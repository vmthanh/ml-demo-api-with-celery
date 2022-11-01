from core.schemas.api_base import APIRequestBase, APIResponseBase


class TripAPIRequestMessage(APIRequestBase):
    PULocationID: int
    DOLocationID: int
    trip_distance: float

    class Config:
        schema_extra = {
            "example": {
                "request_id": "99999",
                "PULocationID": 130,
                "DOLocationID": 250,
                "trip_distance": 3.0,
            }
        }


class TripAPIResponseMessage(APIResponseBase):
    duration: float

    class Config:
        schema_extra = {"example": {"reply_code": 0, "duration": 12.785509620119132}}
