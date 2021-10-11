import abc
from domain import User
from sqlalchemy import select, between


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
        await self.session.add(user)

    async def get(self, email):
        smtm = select(User).where(User.email==email)
        return self.session.execute(smtm).first()

    def list(self):
        return self.session.query(User).all()
