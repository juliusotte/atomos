import abc
from typing import List


class Notification(abc.ABC):
    @abc.abstractmethod
    async def notify(self, destination: str, message: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def broadcast(self, destinations: List[str], message: str):
        raise NotImplementedError
