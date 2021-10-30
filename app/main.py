from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search.api import search
from user.api import user


def create_app():

    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(search)
    app.include_router(user)
    return app
