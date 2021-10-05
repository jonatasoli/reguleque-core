import inspect
from typing import Callable
from user import orm
from user import unit_of_work

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        oauth2: OAuth2PasswordBearer,
        pwd_context = CryptContext,
    ):
       self.uow = uow
       self.oauth2_scheme = oauth2
       self.pwd_context = pwd_context


def bootstrap(
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    oauth2: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="access_token"),
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto"),
) -> MessageBus:

    return MessageBus(
        uow=uow,
        oauth2=oauth2,
        pwd_context=pwd_context,
    )



