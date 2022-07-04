import abc
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Callable, Type

from atomos.service.uow import unit_of_work
from atomos.adapters.orm import factory
from atomos.adapters.repository import sqlalchemy_repository

SessionFactory = Callable[..., Session]

T = TypeVar('T', bound=sqlalchemy_repository.SQLAlchemyRepository)


class SQLAlchemyUnitOfWork(Generic[T], unit_of_work.UnitOfWork[T], abc.ABC):
    def __init__(
        self,
        repository_factory: Type[sqlalchemy_repository.SQLAlchemyRepository],
        session_factory: SessionFactory = factory.DEFAULT_SESSION_FACTORY,
    ):
        self.repository_factory: Type[sqlalchemy_repository.SQLAlchemyRepository] = repository_factory
        self.session_factory: SessionFactory = session_factory

    async def __aenter__(self):
        self.session: Session = self.session_factory()
        self.repository: T = self.repository_factory(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        self.session.close()

    async def _commit(self):
        self.session.commit()

    async def _rollback(self):
        self.session.rollback()
