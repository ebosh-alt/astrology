from pydantic import BaseModel


class PersonData(BaseModel):
    name: str = None
    date: str = None
    time: str = None
    country: str = None
    city: str = None
    theme: str = None


class MailingData(BaseModel):
    online_broadcast: bool = True
    horoscope: bool = True
    video: bool = True
    articles: bool = True
