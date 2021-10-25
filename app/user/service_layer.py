from domain import User, Login, SignUp, Token, UserException, AuthException
from user.unit_of_work import AbstractUnitOfWork

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
        encoded_jwt = await Auth.get_access_token(user_token=_user)
        return dict(
            token=encoded_jwt,
            token_type="bearer",
            role=_user.get('role_id'),
            id=_user.get('id'),
            name=_user.get('name'),
            subscribe="Free User",
            expiration="12-12-2022",
            limits="10 searchs per week"
        )

    @staticmethod
    async def login(uow: AbstractUnitOfWork, user_in: Login):
        _user = await Auth.check_existent_user(
            uow=uow,
            user_in=user_in
        )
        encoded_jwt = await Auth.get_access_token(user_token=_user)
        role = _user.get('role_id')
        return dict(
            token=encoded_jwt,
            token_type="bearer",
            role=role,
            id=_user.get('id'),
            name=_user.get('name'),
            subscribe="Free User",
            expiration="12-12-2022",
            limits="10 searchs per week"
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
                    raise UserException(
                        f"Password not found {user_in.email}"
                    )
            _user = _user.to_app_json()
        return _user

    @staticmethod
    async def get_access_token(user_token):
        to_encode = user_token.copy()
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
    async def check_auth_user(uow, token):
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

