from domain import Login, SignUp, Token


class Auth:

    async def signup(self, user_in: SignUp):
        print(user_in.dict())
        return {"message": "user create with id 1"}

    async def login(self, user_in: Login):
        print(user_in.dict())
        return {"message": "login"}

    async def dashboard(self, token: Token):
        print(token)
        return dict(
            user_id=1,
            name="John Doe",
            subscribe="Free"
        )
