import logging
from sqlalchemy import Column, String, BigInteger, Float, Boolean, Integer
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Profile(Base):
    __tablename__ = "profiles"

    id: int = Column(Integer, autoincrement="auto", primary_key=True)
    user_id: int = Column(BigInteger)
    name: str = Column(String)
    country: str = Column(String)
    city: str = Column(String)
    birth_data: str = Column(String)
    birth_time: str = Column(String)

    def dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "name": self.name,
                "city": self.city,
                "birth_data": self.birth_data
                }


class Profiles(BaseDB):
    async def new(self, profile: Profile):
        await self._add_obj(profile)

    async def get(self, id: int) -> Profile | None:
        result = await self._get_object(Profile, id)
        return result

    async def update(self, profile: Profile) -> None:
        await self._update_obj(instance=profile, obj=Profile)

    async def delete(self, profile: Profile) -> None:
        await self._delete_obj(instance=profile)

    async def in_(self, id: int) -> Profile | bool:
        result = await self.get(id)
        if type(result) is Profile:
            return result
        return False

    async def get_all(self) -> list[Profile]:
        objs = await self._get_objects(obj=Profile)
        return objs

    async def get_by_user(self, user_id: int) -> list[Profile]:
        filters = {
            Profile.user_id: user_id
        }
        profiles = await self._get_objects(obj=Profile, filters=filters)
        return profiles
