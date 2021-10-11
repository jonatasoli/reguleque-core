from domain import User, Login, SignUp, Token
from user.unit_of_work import AbstractUnitOfWork


class Auth:

    @staticmethod
    async def signup(uow: AbstractUnitOfWork, user_in: SignUp):
        async with uow:
            await uow.users.add(user_in)
            await uow.commit()
        return {"message": f"user create"}

    @staticmethod
    async def login(user_in: Login):
        print(user_in.dict())
        return {"message": "login"}

    @staticmethod
    async def dashboard(token: Token):
        print(token)
        return dict(
            user_id=1,
            name="John Doe",
            subscribe="Free"
        )


    @staticmethod
    async def check_existent_user(uow, email):
        async with uow:
            _user = await uow.users.get(email)
        return _user


