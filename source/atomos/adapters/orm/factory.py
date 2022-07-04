from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Callable

from atomos import config

DEFAULT_ENGINE: Engine = create_engine(
    config.DB_URI,
    future=True,
    echo=False,
)

DEFAULT_SESSION_FACTORY: Callable[..., Session] = sessionmaker(
    bind=DEFAULT_ENGINE,
)
