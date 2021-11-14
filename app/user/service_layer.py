from domain import User, Login, SignUp, Token, UserException, AuthException, UserNotFound, UserNotMatchPassword
from user.unit_of_work import AbstractUnitOfWork
from user.schemas import SubscribePlanDB, SubscribeDB, UserDB

from user.adapters.convert_timestamp import convert_str_datetime, convert_datetime_str

from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import timedelta, datetime
from loguru import logger
from config import settings


class Auth:

    @staticmethod
    async def signup(uow: AbstractUnitOfWork, user_in: SignUp):
        _user = None
        async with uow:
            await uow.users.add(user_in)
            await uow.commit()
            _user = await Auth.check_existent_user(
                uow=uow,
                user_in=user_in
            )
            _plan = await uow.users.get_subscribe_plan(id=_user.subscribe_plan_id)
            _subscribe = await uow.users.get_subscribe(id=_plan.subscribe_id)
        encoded_jwt = await Auth.get_access_token(user_token=_user)
        return dict(
            token=encoded_jwt,
            token_type="bearer",
            role=_user.role_id,
            id=_user.id,
            name=_user.name,
            email=_user.email,
            subscribe=_plan.id,
            expiration=convert_datetime_str(_plan.expiration),
            limits=_subscribe.limits
        )

    @staticmethod
    async def login(uow: AbstractUnitOfWork, user_in: Login):
        _user = await Auth.check_existent_user(
            uow=uow,
            user_in=user_in
        )
        encoded_jwt = await Auth.get_access_token(user_token=_user)

        async with uow:
            _plan = await uow.users.get_subscribe_plan(id=_user.subscribe_plan_id)
            _subscribe = await uow.users.get_subscribe(id=_plan.subscribe_id)

        return dict(
            token=encoded_jwt,
            token_type="bearer",
            role=_user.role_id,
            id=_user.id,
            name=_user.name,
            email=_user.email,
            subscribe=_plan.id,
            expiration=convert_datetime_str(_plan.expiration),
            limits=_subscribe.limits
        )


    @staticmethod
    async def dashboard(uow: AbstractUnitOfWork, token: Token):
        _user = await Auth.check_auth_user(uow=uow,token=token)
        return _user

    @staticmethod
    async def check_existent_user(uow, user_in):
        if not user_in.password:
            raise Exception("User not password")
        async with uow:
            _user = await uow.users.get(user_in.email)
            if _user:
                logged = _user.verify_password(user_in.password.get_secret_value())
                if not logged:
                    raise UserNotMatchPassword(
                        f"Password not match {user_in.email}"
                    )
            else:
                raise UserNotFound(
                    f"User not found in database with email {user_in.email}"
                )
            _user = UserDB.from_orm(_user)
        return _user

    @staticmethod
    async def get_access_token(user_token):
        to_encode = user_token.dict().copy()
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )


    @staticmethod
    async def check_auth_user(uow: AbstractUnitOfWork, token: str):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("email")
            if email is None:
                raise UserException("Email not found!")
        except JWTError as e:
            logger.error(e)
            raise AuthException("Token is not authorized!")

        return payload

    @staticmethod
    async def get_subscribe_plan(uow: AbstractUnitOfWork, id: int):
        if not id:
            raise Exception("Id not found")
        async with uow:
            _plan = await uow.users.get_subscribe_plan(id=id)
            if not _plan:
                raise UserException(
                    f"Plan id not found {id}"
                )
            _plan = SubscribePlanDB.from_orm(_plan)
        return _plan


    @staticmethod
    async def get_subscribe(uow: AbstractUnitOfWork, id: int):
        if not id:
            raise Exception("Subscribe ID not found")
        async with uow:
            _subscribe = await uow.users.get_subscribe(id=id)
            if not _subscribe:
                raise UserException(
                    f"Subscribe ID not found {id}"
                )
            _subscribe = SubscribeDB.from_orm(_subscribe)
        return _subscribe

