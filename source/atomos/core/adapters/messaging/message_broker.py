import abc
import logging
from typing import Callable, Awaitable

from atomos.core.domain.events import event

logger = logging.getLogger(__name__)


class MessageBroker(abc.ABC):
    @abc.abstractmethod
    async def publish(self, channel: str, event: event.Event):
        logger.info('publishing: channel=%s, events=%s', channel, event)
        raise NotImplementedError

    @abc.abstractmethod
    async def subscribe(self, channel: str):
        logger.info('subscribing: channel=%s', channel)
        raise NotImplementedError

    @abc.abstractmethod
    async def process(self, handle: Callable[..., Awaitable]):
        raise NotImplementedError
