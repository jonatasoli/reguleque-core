import pytest
import httpx
from functools import wraps
from dynaconf import settings
from loguru import logger
from datetime import datetime, timedelta
from typing import Optional



from user.unit_of_work import AbstractUnitOfWork
from user.repository import AbstractRepository
from domain import SignUp, User, Role
from user.service_layer import Auth


class FakeRepository(AbstractRepository):
    def __init__(self, user):
        self._user = set(user)
        self.id = 0

    async def add(self, user):
        self.id +=1
        self._user.add(user)
        user.id = self.id
        return user

    async def get(self, email):
        return next(b for b in self._user if b.email == email)

    async def list(self):
        return list(self._user)


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeRepository([])
        self.committed = False

    async def _commit(self):
        self.committed = True

    async def rollback(self):
        pass


@pytest.mark.asyncio
async def test_create_user():
    uow = FakeUnitOfWork()
    db_user = User(
        name="John Doe",
        email="test@email.com",
        password="asdasd",
    )
    output = await Auth.signup(uow=uow, user_in=db_user)
    assert output is not None
    assert uow.users.get("test@email.com") is not None
    assert uow.committed



@pytest.mark.asyncio
async def test_check_existent_user():
    uow = FakeUnitOfWork()
    db_user = User(
        name="John Doe",
        email="test@email.com",
        password="asdasd",
    )
    await Auth.signup(uow=uow, user_in=db_user)
    output = await Auth.check_existent_user(uow=uow, email="test@email.com")
    assert uow.users.get("test@email.com") is not None
    assert output is not None
    assert db_user == output


# @pytest.mark.asyncio
# def get_user():
#     db_user = _get_user(db=db, document=document)
#     if not password:
#         raise Exception("User not password")
#     if db_user and db_user.verify_password(password):
#         return db_user
#     else:
#         raise Exception(f"User not finded {db_user.document}, {db_user.password}")



# def authenticate_user(db, document: str, password: str):
#     user = get_user(db, document, password)
#     user_dict = UserSchema.from_orm(user).dict()

#     user = UserInDB(**user_dict)
#     logger.debug(f"{user} ")
#     if not user:
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
#     )
#     return encoded_jwt


# def get_current_user(
#     token: str,
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         document: str = payload.get("sub")
#         if document is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     db = get_session()()

#     user = _get_user(db, document=document)
#     if user is None:
#         raise credentials_exception
#     return user


# def _get_user(db: Session, document: str):
#     try:

#         return db.query(User).filter_by(document=document).first()

#     except Exception as e:
#         raise e


# def check_token(f):
#     @wraps(f)
#     def check_jwt(*args, **kwargs):
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(
#                 kwargs.get("token", None),
#                 settings.SECRET_KEY,
#                 algorithms=[settings.ALGORITHM],
#             )
#             _user_credentials: str = payload.get("sub")
#             if not payload or _user_credentials is None:
#                 raise credentials_exception
#         except JWTError:
#             raise credentials_exception
#         return f(*args, **kwargs)

#     return check_jwt


# def get_role_user(db: Session, user_role_id: int):
#     _role = db.query(Role).filter_by(id=user_role_id).first()
#     return _role.role


# def register_payment_address(db: Session, checkout_data: CheckoutSchema, user):
#     try:
#         _address = (
#             db.query(Address)
#             .filter(
#                 and_(
#                     Address.user_id == user.id,
#                     Address.zipcode == checkout_data.get("zip_code"),
#                     Address.street_number == checkout_data.get("address_number"),
#                     Address.address_complement
#                     == checkout_data.get("address_complement"),
#                     Address.category == "billing",
#                 )
#             )
#             .first()
#         )
#         if not _address:
#             db_payment_address = Address(
#                 user_id=user.id,
#                 country=checkout_data.get("country"),
#                 city=checkout_data.get("city"),
#                 state=checkout_data.get("state"),
#                 neighborhood=checkout_data.get("neighborhood"),
#                 street=checkout_data.get("address"),
#                 street_number=checkout_data.get("address_number"),
#                 zipcode=checkout_data.get("zip_code"),
#                 type_address="house",
#                 category="billing",
#             )
#             db.add(db_payment_address)
#             db.commit()
#             _address = db_payment_address
#         return _address
#     except Exception as e:
#         db.rollback()
#         raise e


# def register_shipping_address(db: Session, checkout_data: CheckoutSchema, user):
#     try:
#         _address = (
#             db.query(Address)
#             .filter(
#                 and_(
#                     Address.user_id == user.id,
#                     Address.zipcode == checkout_data.get("ship_zip"),
#                     Address.street_number == checkout_data.get("ship_number"),
#                     Address.address_complement
#                     == checkout_data.get("ship_address_complement"),
#                     Address.category == "shipping",
#                 )
#             )
#             .first()
#         )

#         if checkout_data.get("shipping_is_payment"):
#             logger.debug(f"{checkout_data}")
#             if not checkout_data.get("ship_zip"):
#                 _address = (
#                     db.query(Address)
#                     .filter(
#                         and_(
#                             Address.user_id == user.id,
#                             Address.zipcode == checkout_data.get("zip_code"),
#                             Address.street_number
#                             == checkout_data.get("address_number"),
#                             Address.address_complement
#                             == checkout_data.get("address_complement"),
#                             Address.category == "billing",
#                         )
#                     )
#                     .first()
#                 )
#             if not _address:
#                 db_shipping_address = Address(
#                     user_id=user.id,
#                     country=checkout_data.get("country"),
#                     city=checkout_data.get("city"),
#                     state=checkout_data.get("state"),
#                     neighborhood=checkout_data.get("neighborhood"),
#                     street=checkout_data.get("address"),
#                     street_number=checkout_data.get("address_number"),
#                     zipcode=checkout_data.get("zip_code"),
#                     type_address="house",
#                     category="shipping",
#                 )
#                 db.add(db_shipping_address)
#                 db.commit()
#                 _address = db_shipping_address
#         else:

#             if not _address:
#                 db_shipping_address = Address(
#                     user_id=user.id,
#                     country=checkout_data.get("ship_country"),
#                     city=checkout_data.get("ship_city"),
#                     state=checkout_data.get("ship_state"),
#                     neighborhood=checkout_data.get("ship_neighborhood"),
#                     street=checkout_data.get("ship_address"),
#                     street_number=checkout_data.get("ship_number"),
#                     zipcode=checkout_data.get("ship_zip"),
#                     type_address="house",
#                     category="shipping",
#                 )
#                 db.add(db_shipping_address)
#                 db.commit()
#                 _address = db_shipping_address

#         logger.debug("INFO")
#         logger.error(f"{_address}")
#         return _address
#     except Exception as e:
#         db.rollback()
#         raise e


# def address_by_postal_code(zipcode_data):
#     try:

#         postal_code = zipcode_data.get("postal_code")

#         if not postal_code:
#             return HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 details={"message": "Cep inválido"},
#             )

#         viacep_url = f"https://viacep.com.br/ws/{postal_code}/json/"
#         status_code = httpx.get(viacep_url).status_code

#         if status_code != 200:
#             return HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail={"message": "Cep inválido"},
#             )

#         response = httpx.get(viacep_url).json()

#         if response.get("erro"):
#             return HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 details={"message": "Cep inválido"},
#             )

#         address = {
#             "street": response.get("logradouro"),
#             "city": response.get("localidade"),
#             "neighborhood": response.get("bairro"),
#             "state": response.get("uf"),
#             "country": COUNTRY_CODE.brazil.value,
#             "zip_code": postal_code,
#         }

#         return address

#     except Exception as e:
#         raise e


# def get_user_login(db: Session, document:str):
#     user = db.query(User).filter_by(document = document).first()
#     return UserSchema.from_orm(user)



# def save_token_reset_password(db: Session, document:str):
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     _token = create_access_token(
#         data={"sub": document}, expires_delta=access_token_expires
#     )
#     _user = db.query(User).filter_by(document = document).first()
#     db_reset = UserResetPassword(
#         user_id = _user.id,
#         token =_token
#     )
#     db.add(db_reset)
#     db.commit()
#     return db_reset


# def reset_password(db: Session, data: UserResponseResetPassword):
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     _user = db.query(User).filter_by(document = data.document).first()
#     _used_token = db.query(UserResetPassword).filter_by(user_id= _user.id).first()
#     _used_token.used_token = True
#     _user.password = pwd_context.hash(data.password)
#     db.commit()
#     return "Senha alterada"
