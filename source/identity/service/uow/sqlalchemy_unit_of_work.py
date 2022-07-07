from atomos.core.service.uow import sqlalchemy_unit_of_work
from atomos.core.adapters.orm import factory

from identity.adapters.repository import sqlalchemy_repository


class SQLAlchemyIdentityUnitOfWork(
    sqlalchemy_unit_of_work.SQLAlchemyUnitOfWork[sqlalchemy_repository.SQLAlchemyIdentityRepository],
):
    def __init__(self, session_factory: sqlalchemy_unit_of_work.SessionFactory = factory.DEFAULT_SESSION_FACTORY):
        super().__init__(sqlalchemy_repository.SQLAlchemyIdentityRepository, session_factory)
