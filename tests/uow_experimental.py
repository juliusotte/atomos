import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Callable

from atomos.core import config

from identity.service.uow import sqlalchemy_unit_of_work
from identity.adapters.orm import orm

logger = logging.getLogger(__name__)

engine: Engine = create_engine(
    #config.DB_URI,
    'postgresql://atomos:secret@localhost:5432/atomos',
    future=True,
    echo=False,
)

session_factory: Callable[..., Session] = sessionmaker(
    bind=engine,
)

uow = sqlalchemy_unit_of_work.SQLAlchemyIdentityUnitOfWork(session_factory)


async def main():
    orm.init_orm(engine)

    async with uow:
        for i in range(0, 10):
            await uow.repository.create_user(f'user-{i}', f'secret-i', f'user-{i}@domain.tld', [])
            await uow.commit()
            user = await uow.repository.get_user(f'user-{1}')
            await uow.repository.create_api_key(user)
            await uow.commit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
