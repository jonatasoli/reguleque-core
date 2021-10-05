from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import MetaData
from loguru import logger

from passlib.context import CryptContext

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from dynaconf import settings

from loguru import logger


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
        server_default="America/Sao_Paulo",
        nullable=True,
    )
    password = Column(String)
    role_id = Column(Integer)
    status = Column(String(20), default="deactivated")
    uuid = Column(String, nullable=True)
    update_email_on_next_login = Column(Boolean, default=False, server_default="0")
    update_password_on_next_login = Column(Boolean, default=False, server_default="0")

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
        return pwd_context.verify(password, self.password)


class UserResetPassword(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    token = Column(String)
    used_token = Column(Boolean, default=False)
