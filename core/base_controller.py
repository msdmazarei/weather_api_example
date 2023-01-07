import typing
from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.datastructures import QueryParams
from pydantic import BaseModel
from sqlalchemy.future import select

from core.base_db_model import BaseDBModel
from core.base_schemas import BaseUpdateSchema
from core.exceptions import NotFoundError, VersionConflictError
from core.generic_schemes import (PaginateMeta, PaginateModelResponse,
                                  SingleModelRespose)
from core.logger import Logger
from core.pagination_options import PaginationOptions
from core.tracing_info import TracingInfo
from core.user import User
from db.session import Base, DBSession
from dependencies import RequestContext, request_context
from dependencies.request_pagination import request_pagination

from .base_context import BaseContext
from .base_filter import BaseFilter

TModel = TypeVar("TModel", bound=BaseDBModel)
TModelSchema = TypeVar("TModelSchema", bound=BaseModel)
TFilter = TypeVar("TFilter", bound=BaseFilter)
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseUpdateSchema)


class BaseController(
    Generic[TModel, TModelSchema, TFilter, TCreateSchema, TUpdateSchema]
):
    model_class: Type[TModel]
    model_schema: Type[TModelSchema]
    context_class: Type[BaseContext[TModel, TFilter, TCreateSchema, TUpdateSchema]]

    def __init__(
        self,
        model_class: Type[TModel],
        model_schema: Type[TModelSchema],
        context_class: Type[BaseContext[TModel, TFilter, TCreateSchema, TUpdateSchema]],
    ):
        self.model_class = model_class
        self.context_class = context_class
        self.model_schema = model_schema

    def get_paginate_meta(
        self, request_context: RequestContext, pagination_options: PaginationOptions
    ) -> PaginateMeta:
        query_params = request_context.request.query_params
        url = request_context.request.url.path
        other_query_dict = {
            k: v
            for k, v in query_params.items()
            if k not in ["page_size", "since", "before"]
        }
        other_query_dict["page_size"] = pagination_options.page_size

        next_page_dict = other_query_dict.copy()
        prev_page_dict = other_query_dict.copy()

        next_page_link = None
        prev_page_link = None
        if pagination_options.since:
            next_page_dict["since"] = pagination_options.since
            next_query_params = QueryParams(**next_page_dict)
            next_page_link = f"{url}?{next_query_params}"

        if pagination_options.before:
            prev_page_dict["before"] = pagination_options.before
            prev_query_params = QueryParams(**prev_page_dict)
            prev_page_link = f"{url}?{prev_query_params}"

        return PaginateMeta(next_page_link, prev_page_link)

    def get_context_by_request(
        self, request_context: RequestContext
    ) -> BaseContext[TModel, TFilter, TCreateSchema, TUpdateSchema]:
        return self.context_class(
            request_context.db_session,
            request_context.tracing_info,
            request_context.user,
            request_context.logger,
        )

    async def paginate(
        self,
        request_context: RequestContext,
        filter: TFilter,
        pagination: PaginationOptions,
    ) -> PaginateModelResponse[TModelSchema]:
        context = self.get_context_by_request(request_context)
        results = await context.paginate(filter, pagination)
        await context.db_session.close()
        new_page_options = pagination.calculate_new_pagination_options(results)
        page_meta = self.get_paginate_meta(request_context, new_page_options)
        data = list(map(self.model_schema.from_orm, results))
        return PaginateModelResponse(meta=page_meta, data=data)

    async def create(
        self,
        data: TCreateSchema,
        request_context: RequestContext,
        commit: bool = True,
    ) -> SingleModelRespose[None, TModelSchema]:
        context = self.get_context_by_request(request_context)
        instance = await context.create(data)
        result = self.model_schema.from_orm(instance)
        if commit:
            await context.db_session.commit()

        return SingleModelRespose(None, result)

    async def update(
        self,
        id: str,
        data: TUpdateSchema,
        request_context: RequestContext,
        commit: bool = True,
    ) -> SingleModelRespose[None, TModelSchema]:
        context = self.get_context_by_request(request_context)
        instance = await context.get(id)
        if instance is None:
            raise NotFoundError()

        instance = await context.update(instance, data)
        result = self.model_schema.from_orm(instance)
        if commit:
            await context.db_session.commit()

        return SingleModelRespose(None, result)

    async def get(
        self, id: str, request_context: RequestContext
    ) -> SingleModelRespose[None, TModelSchema]:
        context = self.get_context_by_request(request_context)
        instance = await context.get(id)
        if instance is None:
            raise NotFoundError()
        return SingleModelRespose(None, self.model_schema.from_orm(instance))

    async def delete(
        self,
        id: str,
        version: int,
        request_context: RequestContext,
        commit: bool = True,
    ) -> SingleModelRespose[None, TModelSchema]:
        context = self.get_context_by_request(request_context)
        instance = await context.get(id)

        if instance is None:
            raise NotFoundError()

        if instance.version != version:
            raise VersionConflictError()

        instance = await context.delete(instance)
        if commit:
            await context.db_session.commit()

        return SingleModelRespose(None, self.model_schema.from_orm(instance))
