from pydantic import BaseModel, SecretStr
from decimal import Decimal
from datetime import datetime


class Login(BaseModel):
    username: str
    password: SecretStr

class SignUp(Login):
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class User:
    def __init__(
        self,
        username,
        password,
        name,
        email,
        role=1,
        update_email_on_next_login=False,
        update_password_on_next_login=False
    ):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.role = role
        self.update_email_on_next_login=update_email_on_next_login,
        self.update_password_on_next_login=update_password_on_next_login,

    def create(self):
        ...

    def update(self):
        ...

    def suspend(self):
        ...


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
