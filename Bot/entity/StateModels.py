from pydantic import BaseModel


class PersonData(BaseModel):
    name: str = None
    country: str = None
    city: str = None
    birth_data: str = None
    birth_time: str = None
    question: str = None
    question_2: str = None
    thema: str = None
    question_status: str = None


class RectificationData(BaseModel):
    time: str = None
    name: str = None
    surname: str = None
    e_mail: str = None
    birth_data: str = None
    birth_time: str = None
    birth_place: str = None
    family: str = None
    illness: str = None
    body_type: str = None
    crossings: str = None
    profession: str = None
    education: str = None
    trips_abroad: str = None
    children: str = None
    edu_grad: str = None
    marriage: str = None
    death_in_family: str = None
    big_deals_losses: str = None
    important_events: str = None
    questions: str = None
    video_link: str = None
    status: str = None