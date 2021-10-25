import uuid
import random
from typing import Any

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from loguru import logger
from passlib.context import CryptContext
from config import settings

from domain import Role


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
metadata = MetaData


@as_declarative()
class Base:
    id: Any
    __name__: str
   # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class User(Base):
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(512))
    email = Column(String(128), unique=True)
    user_timezone = Column(
        String(50),
        default="America/Sao_Paulo",
        nullable=True,
    )
    password = Column(String)
    role_id = Column(Integer, default=Role.FREE_USER.value)
    status = Column(String(20), default="activated")
    uuid = Column(String, nullable=True, unique=True, default=str(random.random()))
    subscribe_plan_id = Column(Integer, ForeignKey("subscribeplan.id"), default=1, server_default="1")

    update_email_on_next_login = Column(Boolean, default=False)
    update_password_on_next_login = Column(Boolean, default=False)

    def to_app_json(self, expand=False):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email,
            "user_timezone": self.user_timezone,
            "role_id": self.role_id,
            "status": self.status,
        }

    def __init__(
        self,
        name=None,
        email=None,
        password=None,
        role_id=None,
        update_email_on_next_login=False,
        update_password_on_next_login=False,
    ):
        super().__init__()
        self.name = name
        self.email = email
        self.role_id = role_id

        self.update_email_on_next_login = update_email_on_next_login
        self.update_password_on_next_login = update_password_on_next_login
        if password is not None:
            self.gen_hash(password)

    def gen_hash(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        from loguru import logger
        logger.debug(f"senha parametro {password}")
        logger.debug(f"senha objeto {self.password}")
        logger.debug(f"{pwd_context.verify(password, self.password)}")
        return pwd_context.verify(password, self.password)

class SubscribePlan(Base):
    id = Column(Integer, primary_key=True)
    subscribe_id=Column(Integer, ForeignKey("subscribe.id"))
    expiration=Column(DateTime())


class Subscribe(Base):
    id = Column(Integer, primary_key=True)
    subscribe=Column(String)
    limits=Column(Text)

class UserResetPassword(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    token = Column(String)
    used_token = Column(Boolean, default=False)
