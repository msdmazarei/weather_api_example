import loguru
from fastapi import Depends, Request

from core.logger import Logger
from core.tracing_info import TracingInfo
from core.user import User
from db.session import DBSession

from .request_db_session import request_db_session
from .request_logger import request_logger
from .request_user import request_user
from .tracing_info import request_tracing_info


class RequestContext:
    db_session: DBSession
    user: User
    tracing_info: TracingInfo
    logger: Logger
    request: Request

    def __init__(
        self,
        db_session: DBSession,
        user: User,
        tracing_info: TracingInfo,
        logger: Logger,
        request: Request,
    ):
        self.db_session = db_session
        self.user = user
        self.tracing_info = tracing_info
        self.logger = logger
        self.request = request


async def request_context(
    request: Request,
    tracing_info: TracingInfo = Depends(request_tracing_info),
    db_session: DBSession = Depends(request_db_session),
    user: User = Depends(request_user),
    logger: Logger = Depends(request_logger),
) -> RequestContext:
    return RequestContext(db_session, user, tracing_info, logger, request)
