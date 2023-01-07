from typing import Any, Tuple

from asyncpg.cursor import Cursor
from sqlalchemy.dialects.postgresql.asyncpg import PGExecutionContext
from sqlalchemy.engine import Engine
from sqlalchemy.event import api
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession as DBSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings


# @event.listens_for(Engine, "before_cursor_execute", retval=True)
def comment_sql_calls(
    conn: AsyncConnection,
    cursor: Cursor,
    statement: str,
    parameters: Any,
    context: PGExecutionContext,
    executemany: bool,
) -> Tuple[str, Any]:
    if "tracing_info" in conn.info:
        statement = statement + f" -- {conn.info['tracing_info']}"

    return statement, parameters


api.listen(Engine, "before_cursor_execute", comment_sql_calls, retval=True)

engine = create_async_engine(settings.database_uri(), echo=True, future=True)
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=DBSession,
)

Base = declarative_base()


__all__ = ["Base", "SessionLocal", "DBSession"]
