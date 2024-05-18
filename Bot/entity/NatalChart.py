from pydantic import BaseModel


class ElementNatalChart(BaseModel):
    planet: str
    # degrees: str
    sign: str
    id_sign: int
    house: int

