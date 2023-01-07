# from typing import TypeVar, Generic
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

TMETA = TypeVar("TMETA")
TMODEL = TypeVar("TMODEL")


class PaginateMeta(BaseModel):
    next_page_link: Optional[str]
    prev_page_link: Optional[str]

    def __init__(self, next_page_link: Optional[str], prev_page_link: Optional[str]):
        d = dict(next_page_link=next_page_link, prev_page_link=prev_page_link)
        BaseModel.__init__(self, **d)


class SingleModelRespose(Generic[TMETA, TMODEL], BaseModel):
    meta: TMETA
    data: TMODEL

    def __init__(self, meta: TMETA, data: TMODEL):
        BaseModel.__init__(self, **dict(meta=meta, data=data))


class PaginateModelResponse(Generic[TMODEL], BaseModel):
    meta: PaginateMeta
    data: list[TMODEL]

    def __init__(self, meta: PaginateMeta, data: list[TMODEL]):
        BaseModel.__init__(self, **dict(meta=meta, data=data))
