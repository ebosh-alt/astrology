import logging
from sqlalchemy import Column, String, BigInteger, Float, Boolean, Integer
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Questionnaire(Base):
    __tablename__ = "admins_chats"

    id: int = Column(Integer, autoincrement="auto", primary_key=True)
    user_id: int = Column(BigInteger)
    name: str = Column(String)
    city: str = Column(String)
    birth_data: str = Column(String)

    def dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "name": self.name,
                "city": self.city,
                "birth_data": self.birth_data
                }


class Questionnaires(BaseDB):
    async def new(self, obj: Questionnaire):
        await self._add_obj(obj)

    async def get(self, id: int) -> Questionnaire | None:
        result = await self._get_object(Questionnaire, id)
        return result

    async def update(self, obj: Questionnaire) -> None:
        await self._update_obj(instance=obj, obj=Questionnaire)

    async def delete(self, obj: Questionnaire) -> None:
        await self._delete_obj(instance=obj)

    async def in_(self, id: int) -> Questionnaire | bool:
        result = await self.get(id)
        if type(result) is Questionnaire:
            return result
        return False
    
    async def get_all(self) -> list[Questionnaire]:
        objs = await self._get_objects(obj=Questionnaire)
        return objs

    async def get_by_user(self, user_id: int) -> list[Questionnaire]:
        filters = {
            Questionnaire.user_id: user_id
        }
        objs = await self._get_objects(obj=Questionnaire, filters=filters)
        return objs