import abc
from sqlalchemy.orm import Session

from atomos.adapters.repository import repository
from atomos.adapters.orm import factory


class SQLAlchemyRepository(repository.Repository, abc.ABC):
    def __init__(self, session: Session = factory.DEFAULT_SESSION_FACTORY()):
        super().__init__()
        self.session: Session = session
