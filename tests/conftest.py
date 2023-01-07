import asyncio
from datetime import datetime, timedelta
from typing import AsyncIterator, Dict

import faker as faker_module
import pytest
import pytest_asyncio
from fastapi import Request
from fastapi.testclient import TestClient
from httpx import AsyncClient, Auth
from sqlalchemy.ext.asyncio import AsyncSession as DBSession

from app import web_app
from core import utils
from core.logger import Logger, get_logger
from core.tracing_info import SourceType, TracingInfo
from core.user import User
from db.session import SessionLocal
from dependencies import RequestContext

faker = faker_module.Faker()
logger_instance = get_logger()


user_counter = int(datetime.utcnow().timestamp())
trace_info_counter = user_counter


@pytest.fixture()
def user() -> User:
    global user_counter
    global faker
    user = User(faker.email())
    user_counter += 1
    return user


@pytest.fixture()
def tracing_info() -> TracingInfo:
    global trace_info_counter
    trace_info_counter += 1
    return TracingInfo(SourceType.HTTPRequest, f"trace-{trace_info_counter}")


@pytest_asyncio.fixture()
async def logger() -> Logger:
    return logger_instance


@pytest_asyncio.fixture()
async def request_context(
    db_session: DBSession,
    user: User,
    tracing_info: TracingInfo,
    logger: Logger,
    request: Request,
) -> RequestContext:
    return RequestContext(db_session, user, tracing_info, logger, request)


@pytest.fixture()
def async_client() -> AsyncClient:
    return AsyncClient(app=web_app, base_url="http://testserver")


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.new_event_loop()
