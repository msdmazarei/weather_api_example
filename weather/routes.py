"""
this module defines route for Weather Resource
"""
from fastapi import APIRouter, Depends

from dependencies.request_context import request_context

from .controller import Controller

controller = Controller()


def get_routes() -> APIRouter:
    prefix = "api"
    router = APIRouter()
    router.add_api_route(f"/{prefix}/weather", controller.paginate, methods=["GET"])
    return router
