import abc
from sqlalchemy import select, between

from user.orm import User
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
        db_user = obj_in_to_db_obj(
            model=User,
            obj_in=user
        )
        return self.session.add(db_user)

    async def get(self, email):
        smtm = select(User).where(User.email==email)
        return await self.session.execute(smtm).one()

    def list(self):
        return self.session.query(User).all()
