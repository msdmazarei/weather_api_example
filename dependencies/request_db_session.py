from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession as DBSession

from core.tracing_info import TracingInfo
from db.session import SessionLocal

from .tracing_info import request_tracing_info


async def request_db_session(
    trace_info: TracingInfo = Depends(request_tracing_info),
) -> AsyncIterator[DBSession]:
    db_session: DBSession = SessionLocal()
    conn = await db_session.connection()
    conn.info["tracing_info"] = trace_info.get_trace_id()
    yield db_session
    await db_session.close()
