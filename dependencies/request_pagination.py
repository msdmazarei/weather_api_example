from typing import Optional

from fastapi import Query

from core.pagination_options import PaginationOptions


async def request_pagination(
    since: Optional[int] = None, before: Optional[int] = None, page_size: int = 50
) -> PaginationOptions:
    return PaginationOptions(since=since, before=before, page_size=page_size)
