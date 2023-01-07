from datetime import datetime
from functools import lru_cache
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request

from core import utils
from core.config import settings
from core.user import User


async def get_user_by_bearer_token(bearer_token: str) -> Optional[User]:
    return None


async def request_user(authorization: str = Header(default="")) -> User:
    return User("anonymous@anonymous.com")
    user = await get_user_by_bearer_token(authorization)
    if user is None:
        raise HTTPException(401)
    return user
