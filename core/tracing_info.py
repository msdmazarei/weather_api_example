from enum import Enum


class SourceType(Enum):
    HTTPRequest: str = "http_request"


class TracingInfo:
    source: SourceType
    trace_id: str

    def __init__(self, source: SourceType, trace_id: str):
        self.source = source
        self.trace_id = trace_id

    def get_trace_id(self) -> str:
        return self.trace_id
