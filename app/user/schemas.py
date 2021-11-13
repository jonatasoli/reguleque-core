from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class SubscribePlanDB(BaseModel):
    id: int
    subscribe_id: int
    expiration: datetime

    class Config:
        orm_mode = True


class SubscribeDB(BaseModel):
    id: int
    subscribe: str
    limits: str

    class Config:
        orm_mode = True


class UserDB(BaseModel):
    id: int
    name: str
    email: str
    user_timezone: str
    password: str
    role_id: int
    status: str
    uuid: str
    subscribe_plan_id: int
    update_email_next_login: Optional[bool]
    update_password_on_next_login: Optional[bool]

    class Config:
        orm_mode = True
