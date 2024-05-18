from pydantic import BaseModel


class PersonData(BaseModel):
    name: str = None
    city: str = None
    birth_data: str = None
