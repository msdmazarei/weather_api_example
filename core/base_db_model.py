from datetime import datetime
from typing import Dict, List

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped

from db.session import Base


class BaseDBModel(Base):
    __abstract__ = True
    id: Mapped[str] = Column(Integer, primary_key=True)
