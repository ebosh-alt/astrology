import logging
from sqlalchemy import Column, String, BigInteger, Float, Boolean, Integer
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class User(Base):
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


class Users(BaseDB):
    async def new(self, obj: User):
        await self._add_obj(obj)

    async def get(self, id: int) -> User | None:
        result = await self._get_object(User, id)
        return result

    async def update(self, obj: User) -> None:
        await self._update_obj(instance=obj, obj=User)

    async def delete(self, obj: User) -> None:
        await self._delete_obj(instance=obj)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False
    
    async def get_all(self) -> list[User]:
        objs = await self._get_objects(obj=User)
        return objs