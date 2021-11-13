from loguru import logger

from fastapi import APIRouter, status, Depends, HTTPException, Header

from domain import Login, SignUp, Token, UserNotMatchPassword, UserNotFound
from user.service_layer import Auth
from user.bootstrap import bootstrap

bootstrap = bootstrap()


user = APIRouter()

@user.post("/user/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    user_in: SignUp,
    auth: Auth = Depends(),
):
    try:
        return await auth.signup(
            uow=bootstrap.uow,
            user_in=user_in
        )
    except Exception as e:
        logger.error(e)
        _detail_msg="Error to process request"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail_msg)


@user.post("/user/login", status_code=status.HTTP_200_OK)
async def login(
    *,
    user_in: Login,
    auth: Auth = Depends()
):
    try:
        return await auth.login(
            uow=bootstrap.uow,
            user_in=user_in
        )
    except UserNotFound as e:
        logger.error(e)
        _detail_msg="User not exist in database"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_detail_msg)
    except UserNotMatchPassword as e:
        logger.error(e)
        _detail_msg="Wrong password"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_detail_msg)
    except Exception as e:
        logger.error(e)
        _detail_msg="Error to process request"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail_msg)


@user.post("/user/dashboard", status_code=status.HTTP_200_OK)
async def dashboard(
    *,
    auth: Auth = Depends(),
    token: str = Header(None),
):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return await auth.dashboard(
            token=token,
            uow=bootstrap.uow
        )
    except Exception as e:
        logger.error(e)
        _detail_msg="Error to process request"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail_msg)
