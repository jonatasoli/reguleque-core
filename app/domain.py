from pydantic import BaseModel, SecretStr
from decimal import Decimal
from datetime import datetime


class Login(BaseModel):
    username: str
    password: SecretStr

class SignUp(Login):
    mail: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class User:
    def __init__(self):
        ...

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
