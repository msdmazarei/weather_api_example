"""
This is Controller Module for Weather API
"""
from fastapi import Depends
from fastapi.datastructures import QueryParams

from core.base_controller import BaseController
from core.exceptions import NotFoundError, VersionConflictError
from core.generic_schemes import (PaginateMeta, PaginateModelResponse,
                                  SingleModelRespose)
from core.pagination_options import PaginationOptions
from dependencies import RequestContext, request_context
from dependencies.request_pagination import request_pagination

from .context import Context
from .model import Weather
from .schemas import DataScheme, Filter


class Controller(BaseController[Weather, DataScheme, Filter, None, None]):
    def __init__(self) -> None:
        BaseController.__init__(self, Weather, DataScheme, Context)

    async def paginate(
        self,
        request_context: RequestContext = Depends(request_context),
        filter: Filter = Depends(),
        pagination: PaginationOptions = Depends(request_pagination),
    ) -> PaginateModelResponse[DataScheme]:
        rtn = await BaseController.paginate(self, request_context, filter, pagination)
        return rtn
