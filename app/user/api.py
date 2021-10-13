from loguru import logger

from fastapi import APIRouter, status, Depends, HTTPException, Header

from domain import Login, SignUp, Token
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
    return await auth.signup(
        uow=bootstrap.uow,
        user_in=user_in
    )


@user.post("/user/login", status_code=status.HTTP_200_OK)
async def login(
    *,
    user_in: Login,
    auth: Auth = Depends()
):
    return await auth.login(
        uow=bootstrap.uow,
        user_in=user_in
    )


@user.post("/user/dashboard", status_code=status.HTTP_200_OK)
async def dashboard(
    *,
    auth: Auth = Depends(),
    token: str = Header(None),
):
    """
{
  "email": "email@kct.com",
  "password": "asdasd"
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsInV1aWQiOiIwLjM5NjQyNDY5OTM0OTc1NzIiLCJuYW1lIjoiSm9uaCBUaGlyZCIsImVtYWlsIjoiZW1haWxAa2N0LmNvbSIsInVzZXJfdGltZXpvbmUiOiJBbWVyaWNhL1Nhb19QYXVsbyIsInJvbGVfaWQiOjEsInN0YXR1cyI6ImFjdGl2YXRlZCIsImV4cCI6MTYzNDEzMTAwNX0.3dgCCY1C46Kg7w8jWp85Jxz-HtvXlhHZi7d6umZICuA"

}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await auth.dashboard(
        token=token,
        uow=bootstrap.uow
    )
