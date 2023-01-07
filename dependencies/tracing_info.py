from fastapi import Header

from core.tracing_info import SourceType, TracingInfo


async def request_tracing_info(x_request_id: str = Header()) -> TracingInfo:
    return TracingInfo(SourceType.HTTPRequest, x_request_id)
