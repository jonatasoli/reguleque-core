from __future__ import annotations
import abc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import repository
from config import settings



class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractRepository

    def __aenter__(self) -> AbstractUnitOfWork:
        return self

    def __aexit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


def session_factory():
    if not hasattr(settings, "DB_DSN_URI"):
        return None
    return sessionmaker(
        expire_on_commit=False,
        class_=AsyncSession,
        bind=create_async_engine(
            settings.DB_DSN_URI,
        )
    )


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=session_factory()):
        self.session_factory = session_factory

    def __aenter__(self):
        self.session = self.session_factory()  # type: Session
        self.products = repository.SqlAlchemyRepository(self.session)
        return super().__aenter__()

    def __aexit__(self, *args):
        super().__aexit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
