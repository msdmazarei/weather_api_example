from __future__ import annotations

import loguru
from fastapi import Depends, Request
from loguru import logger

from core.tracing_info import TracingInfo

from .tracing_info import request_tracing_info


async def request_logger(
    request: Request, tracing_info: TracingInfo = Depends(request_tracing_info)
) -> "loguru.Logger":
    if request.client is not None:
        return logger.bind(
            request_id=tracing_info.get_trace_id(),
            client_addr=f"{request.client.host}:{request.client.port}",
        )
    return logger
