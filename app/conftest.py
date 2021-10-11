import sys
from os.path import abspath
from os.path import dirname as d

import pytest
import asyncio
from fastapi.testclient import TestClient

from config import settings
from user.orm import Base, get_engine_main
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from main import create_app as app
root_dir = d(abspath(__file__))
sys.path.append(root_dir)

meta = Base.metadata

@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="function")
async def apply_migrations() -> None:
    engine=get_engine_main()
    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


@pytest.fixture(scope="function")
def postgres_session():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")
    return sessionmaker(
        expire_on_commit=False,
        class_=AsyncSession,
        bind=create_async_engine(
            settings.DB_DSN_URI,
        )
    )

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture
def client():
    with TestClient(app()) as client:
        yield client
