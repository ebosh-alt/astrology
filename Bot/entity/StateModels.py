from pydantic import BaseModel


class PersonData(BaseModel):
    name: str = None
    city: str = None
    birth_data: str = None


class MailingData(BaseModel):
    online_broadcast: bool = True
    horoscope: bool = True
    video: bool = True
    articles: bool = True
