from datetime import date, datetime

from pydantic import BaseModel
from sqlalchemy.sql import Select

from core.base_filter import BaseFilter

from .model import Weather


class DataScheme(BaseModel):
    id: int
    station: str
    measure_date: datetime
    max_temperature: int | None
    min_temperature: int | None
    precipitation_mm: int | None

    class Config:
        orm_mode = True


class Filter(BaseModel, BaseFilter):
    station_name: str | None
    measure_date: date | None

    def apply_on_query(self, query: Select) -> Select:
        rtn = query

        if self.station_name:
            rtn = rtn.where(Weather.station == self.station_name)

        if self.measure_date:
            rtn = rtn.where(Weather.measure_date == self.measure_date)

        return rtn
