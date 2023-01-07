from pydantic import BaseModel


class BaseUpdateSchema(BaseModel):
    version: int
