from pydantic import BaseModel


class ElementNatalChart(BaseModel):
    planet: str
    sign: str
    id_sign: int
    house: int

