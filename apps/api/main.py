from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

import config
from apps.api.api_routers import api_router
from core.utilities.cls_loguru_config import loguru_setting

loguru_setting.setup_app_logging()

app = FastAPI(title=config.PROJECT_NAME, version=config.APP_VERSION)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    base_error_message = f"Falied to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                "message": f"{base_error_message}",
                "detail": exc.errors(),
                "body": exc.body,
            }
        ),
    )


@app.exception_handler(Exception)
def server_exception_handler(request: Request, exc: Exception):
    base_error_message = f"Falied to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"message": f"{base_error_message}. Detail: {exc}"}),
    )


app.include_router(api_router)
