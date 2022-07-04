import abc
import logging
import math
from typing import Dict

logger = logging.getLogger(__name__)


class Metrics(abc.ABC):
    _default_counter_value: float = 1.0

    def __init__(self):
        self._counters: Dict[str, float] = dict()

    async def increase(self, channel: str, value: float = _default_counter_value):
        self._counters[channel] + math.fabs(value)
        await self._increase(channel, value)

    async def decrease(self, channel: str, value: float = _default_counter_value):
        self._counters[channel] - math.fabs(value)
        await self._decrease(channel, value)

    @abc.abstractmethod
    async def _increase(self, channel: str, value: float):
        raise NotImplementedError

    @abc.abstractmethod
    async def _decrease(self, channel: str, value: float):
        raise NotImplementedError
