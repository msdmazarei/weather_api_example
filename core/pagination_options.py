from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError, root_validator, validator
from sqlalchemy import desc
from sqlalchemy.sql import Select

from core import utils
from core.utils import to_epoch_us

from .base_db_model import BaseDBModel

MAX_PAGE_SIZE = 100

T = TypeVar("T", bound=BaseDBModel)


class PaginationOptions(BaseModel):
    since: Optional[int]
    before: Optional[int]
    page_size: int

    @validator("page_size")
    def page_size_must_be_lesser_than_max(cls, v: int) -> int:
        if v > MAX_PAGE_SIZE:
            raise ValueError(f"page_size must be lesser that {MAX_PAGE_SIZE}")
        return v

    @root_validator
    def one_of_since_or_before_must_be_provided(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        since, before = values.get("since"), values.get("before")
        return values

    def apply_on_query(self, cls: Type[BaseDBModel], query: Select) -> Select:

        if self.since is not None:
            query = query.where(cls.id < self.since).order_by(desc(cls.id))
        elif self.before is not None:
            query = query.where(cls.id > self.before).order_by(cls.id)
        else:
            query = query.order_by(desc(cls.id))

        query = query.limit(self.page_size)
        return query

    def calculate_new_pagination_options(self, items: List[T]) -> "PaginationOptions":
        rtn = PaginationOptions(page_size=self.page_size)
        if len(items) == 0:
            rtn.since = self.before
            rtn.before = self.since
            return rtn

        first_index, last_index = 0, -1

        if len(items) > 0 and len(items) < self.page_size:
            rtn.since = None
        else:
            rtn.since = items[last_index].id

        if len(items) > 0:
            rtn.before = items[first_index].id
        return rtn
