from pydantic import BaseModel


class APIRequestBase(BaseModel):
    request_id: str


class APIResponseBase(BaseModel):
    reply_code: int
