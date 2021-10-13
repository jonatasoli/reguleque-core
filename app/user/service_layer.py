from domain import User, Login, SignUp, Token, UserException
from user.unit_of_work import AbstractUnitOfWork

from jose import JWTError, jwt
from fastapi import HTTPException, status
from datetime import timedelta, datetime
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
            role=_user.get('role_id')
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
            role=role
        )

    @staticmethod
    async def dashboard(token: Token):
        print(token)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return dict(
            user_id=1,
            name="John Doe",
            subscribe="Free"
        )


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
