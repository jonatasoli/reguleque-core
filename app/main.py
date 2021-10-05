from typing import Optional

from fastapi import FastAPI
from search.api import search
from user.api import user


def create_app():
    app = FastAPI()
    app.include_router(search)
    app.include_router(user)
    return app
