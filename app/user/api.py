from loguru import logger

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from domain import Login, SignUp, Token
from user.service_layer import Auth


user = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")

@user.post("/user/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    user_in: SignUp,
    auth: Auth = Depends()
):
    return await auth.signup(user_in)


@user.post("/user/login", status_code=status.HTTP_200_OK)
async def login(
    *,
    user_in: Login,
    auth: Auth = Depends()
):
    return await auth.login(user_in)


@user.post("/user/dashboard", status_code=status.HTTP_200_OK)
async def dashboard(
    *,
    token: str = Depends(oauth2_scheme),
    auth: Auth = Depends()
):
   return await auth.dashboard(token)
