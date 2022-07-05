from __future__ import annotations
import abc
import contextlib
from typing import TypeVar, Generic

from atomos.core.adapters.repository import repository

T = TypeVar('T', bound=repository.Repository)


class UnitOfWork(Generic[T], contextlib.AbstractAsyncContextManager, abc.ABC):
    repository: T

    async def __aenter__(self) -> UnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self._commit()

    async def rollback(self):
        await self._rollback()

    def collect_new_events(self):
        for entity in self.repository.collected_entities:
            while entity.events:
                yield entity.events.pop(0)

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self):
        raise NotImplementedError
