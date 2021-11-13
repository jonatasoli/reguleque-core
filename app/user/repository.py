import abc
from sqlalchemy import select, between

from user.orm import User, Subscribe, SubscribePlan
from user.schemas import SubscribePlanDB, SubscribeDB, UserDB
from user.adapters.db_obj_converter import obj_in_to_db_obj


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, user):
        db_user = User(
            name=user.name,
            password=user.password.get_secret_value(),
            email=user.email,
        )
        return self.session.add(db_user)

    async def get(self, email):
        smtm = select(User).where(User.email==email)
        _result =await self.session.execute(smtm)
        return _result.scalars().first()

    async def get_subscribe(self, id):
        smtm = select(Subscribe).where(Subscribe.id==id)
        _result =await self.session.execute(smtm)
        return SubscribeDB.from_orm(_result.scalars().first())

    async def get_subscribe_plan(self, id):
        smtm = select(SubscribePlan).where(SubscribePlan.id==id)
        _result =await self.session.execute(smtm)
        return SubscribePlanDB.from_orm(_result.scalars().first())

    def list(self):
        return self.session.query(User).all()
