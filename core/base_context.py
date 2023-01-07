import typing
from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy.future import select

from core.base_db_model import BaseDBModel
from core.base_schemas import BaseUpdateSchema
from core.exceptions import NotFoundError, VersionConflictError
from core.logger import Logger
from core.pagination_options import PaginationOptions
from core.tracing_info import TracingInfo
from core.user import User
from db.session import Base, DBSession

from .base_filter import BaseFilter

TModel = TypeVar("TModel", bound=BaseDBModel)
TFilter = TypeVar("TFilter", bound=BaseFilter)
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseUpdateSchema)


class BaseContext(Generic[TModel, TFilter, TCreateSchema, TUpdateSchema]):
    db_session: DBSession
    trace_info: TracingInfo
    user: User
    entity_type: str
    logger: Logger
    model_class: Type[TModel]

    def __init__(
        self,
        db_session: DBSession,
        trace_info: TracingInfo,
        user: User,
        logger: Logger,
        model_class: Type[TModel],
    ):
        self.db_session = db_session
        self.trace_info = trace_info
        self.user = user
        self.logger = logger
        self.model_class = model_class
        self.entity_type = f"{model_class.__module__}.{model_class.__qualname__}"

    async def get(self, id: Union[str, UUID]) -> Optional[TModel]:
        result = await self.db_session.get(self.model_class, id)
        return result

    async def paginate(
        self, filter: TFilter, pagination_options: PaginationOptions
    ) -> List[TModel]:
        query = select(self.model_class)
        query = filter.apply_on_query(query)
        query = pagination_options.apply_on_query(self.model_class, query)
        result = await self.db_session.execute(query)

        rtn = [i for (i,) in result.fetchall()]
        if pagination_options.before is not None:
            rtn.reverse()
        return rtn
