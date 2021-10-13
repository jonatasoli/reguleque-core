import enum
from pydantic import BaseModel, SecretStr
from decimal import Decimal
from datetime import datetime


class Role(enum.Enum):
    FREE_USER = 1
    PAID_PLAN_BASIC = 2
    ADMIN = 50

class Login(BaseModel):
    email: str
    password: SecretStr

class SignUp(Login):
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class User:
    def __init__(
        self,
        password,
        name,
        email,
        id=None,
        role=1,
        update_email_on_next_login=False,
        update_password_on_next_login=False
    ):
        self.id = id
        self.password = password
        self.name = name
        self.email = email
        self.role = role
        self.update_email_on_next_login=update_email_on_next_login,
        self.update_password_on_next_login=update_password_on_next_login,

    def __call__(self):
        return self.__dict__()

    def __repr__(self):
        return f"name={self.name}, email={self.email}"

    def __dict__(self):
        return dict(name=self.name, email=self.email)

    def create(self):
        return dict(name=self.name, email=self.email, password=self.password)

    def upgrade(self):
        self.role = Role.PAID_PLAN_BASIC.value

    def upgrade_admin(self):
        self.role = Role.ADMIN.value

    def downgrade(self):
        self.role = Role.FREE_USER.value


class Auth:
    def __init__(self):
        ...

    def login(self):
        ...

    def sign_up(self):
        ...

    def check_toke(self):
        ...


class Admin:

    def __init__(self):
        ...

    def upgrade_user(self):
        ...

    def downgrade_user(self):
        ...

    def update_user(self):
        ...

    def delete_user(self):
        ...

    def create_payment_message(self):
        ...

    def update_payment_message(self):
        ...


class UserException(Exception):
    ...
