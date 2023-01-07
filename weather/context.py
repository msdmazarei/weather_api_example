from sqlalchemy.ext.asyncio import AsyncSession as SQLSession

from core.base_context import BaseContext
from core.logger import Logger
from core.tracing_info import TracingInfo
from core.user import User

from .model import Weather
from .schemas import Filter


class Context(BaseContext[Weather, Filter, None, None]):
    def __init__(
        self,
        db_session: SQLSession,
        trace_info: TracingInfo,
        user: User,
        logger: Logger,
    ):
        BaseContext.__init__(self, db_session, trace_info, user, logger, Weather)
