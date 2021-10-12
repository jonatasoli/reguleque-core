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
    async def login(uow: AbstractUnitOfWork, user_in: Login):
        print(user_in.dict())
        logged = False
        if not user_in.password:
            raise Exception("User not password")
        async with uow:
            _user = await uow.users.get(user_in.email)
            if _user:
                logged = _user.verify_password(user_in.password.get_secret_value())
            _user = _user.to_app_json()

        if logged:
            return _user
        else:
            raise Exception(f"User not finded {user_in.email}, {user_in.password}")

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


