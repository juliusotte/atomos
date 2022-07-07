import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Callable

from atomos.core import config

from identity.adapters.repository import sqlalchemy_repository
from identity.adapters.orm import orm

logger = logging.getLogger(__name__)

engine: Engine = create_engine(
    config.DB_URI,
    future=True,
    echo=False,
)

session_factory: Callable[..., Session] = sessionmaker(
    bind=engine,
)

session = session_factory()
repository = sqlalchemy_repository.SQLAlchemyIdentityRepository(session)


async def main():
    orm.init_orm(engine)

    for i in range(0, 10):
        await repository.create_permission(f'p-{i}')
        await repository.create_role(f'r-{i}', [])
        await repository.create_user(f'u-{i}', 'secret', f'u-{i}@domain.tld', [])
        logger.debug(f'completed iteration: {i}')
    repository.session.commit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
