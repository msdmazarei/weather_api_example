from sqlalchemy import JSON, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import Mapped

from core.base_db_model import BaseDBModel
from db.session import Base


class Weather(BaseDBModel):
    __tablename__ = "weather"
    # TODO: if any other datamodel uses station value, its better for normalization to separate it to another table and use FK here
    station = Column(String, nullable=False)
    measure_date = Column(TIMESTAMP, nullable=False)
    max_temperature = Column(Integer, nullable=True)
    min_temperature = Column(Integer, nullable=True)
    precipitation_mm = Column(Integer, nullable=True)
