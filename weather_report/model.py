from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Mapped

from core.base_db_model import BaseDBModel
from db.session import Base


class WeatherReport(BaseDBModel):
    __tablename__ = "agg_weather_report"
    station = Column(String, nullable=False)
    measure_year = Column(Integer, nullable=False)
    max_temperature = Column(Integer, nullable=True)
    min_temperature = Column(Integer, nullable=True)
    total_precipitation_cm = Column(Float, nullable=True)
