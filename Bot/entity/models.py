from typing import NamedTuple

from pydantic import BaseModel


class Date(BaseModel):
    year: str
    month: str
    day: str
    hour: str
    minute: str


