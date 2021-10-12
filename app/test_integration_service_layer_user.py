import pytest
from config import settings
from loguru import logger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


from user.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from user.repository import AbstractRepository, SqlAlchemyRepository
from domain import SignUp, User, Role
from user.service_layer import Auth
from user.orm import get_session


@pytest.mark.asyncio
async def test_database(apply_migrations):
    dir(apply_migrations)
    assert True == True


@pytest.mark.db
@pytest.mark.asyncio
async def test_create_user(apply_migrations, postgres_session):
    uow = SqlAlchemyUnitOfWork(session_factory=postgres_session)
    db_user = SignUp(
        name="John Doe",
        email="test@email.com",
        password="asdasd",
    )
    output = await Auth.signup(uow=uow, user_in=db_user)
    assert output is not None
    assert uow.users.get("test@email.com") is not None



@pytest.mark.skip
@pytest.mark.db
@pytest.mark.asyncio
async def test_check_existent_user(apply_migrations, postgres_session):
    uow = SqlAlchemyUnitOfWork(session_factory=postgres_session)
    # db_user = User(
    #     name="John Carmac",
    #     email="test2@email.com",
    #     password="asdasd",
    # )
    # await Auth.signup(uow=uow, user_in=db_user)
    db_user = User(
        name="John Doe",
        email="test@email.com",
        password="asdasd",
    )
    output = Auth.check_existent_user(uow=uow, email="test@email.com")
    import ipdb; ipdb.set_trace()
    assert uow.users.get("test@email.com") is not None
    assert output is not None
    assert db_user == output
