from datetime import date, datetime

from pydantic import BaseModel
from sqlalchemy.sql import Select

from core.base_filter import BaseFilter

from .model import WeatherReport


class DataScheme(BaseModel):
    id: int
    station: str
    measure_year: int
    max_temperature: int | None
    min_temperature: int | None
    total_precipitation_cm: float | None

    class Config:
        orm_mode = True


class Filter(BaseModel, BaseFilter):
    station_name: str | None
    measure_year: int | None

    def apply_on_query(self, query: Select) -> Select:
        rtn = query

        if self.station_name:
            rtn = rtn.where(WeatherReport.station == self.station_name)

        if self.measure_year:
            rtn = rtn.where(WeatherReport.measure_year == self.measure_year)

        return rtn
