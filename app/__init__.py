from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm.exc import StaleDataError

from asgi_middlewares.request_id_middleware import RequestIDMiddleware
from core.config import ENV, settings
from core.exceptions import ConflictError, VersionConflictError
from weather.routes import get_routes as weather_routes
from weather_report.routes import get_routes as weather_report_routes

now_epoch = int(datetime.utcnow().timestamp())
web_app = FastAPI(
    debug=settings.get_env() == ENV.DEV,
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
)

web_app.include_router(weather_routes())
web_app.include_router(weather_report_routes())
web_app.add_middleware(
    RequestIDMiddleware,
    x_request_id_header=settings.X_REQ_ID_HEADER,
    counter_prefix=f"{settings.APP_ID}-{now_epoch}",
)


@web_app.exception_handler(ValidationError)
async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
