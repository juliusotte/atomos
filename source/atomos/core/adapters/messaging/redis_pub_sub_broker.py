import redis
import json
from dataclasses import asdict
from typing import Callable, Awaitable

from atomos.core import config
from atomos.core.adapters.messaging import message_broker
from atomos.domain.events import event


class RedisPubSubBroker(message_broker.MessageBroker):
    def __init__(self, host: str = config.REDIS_HOST, port: int = config.REDIS_PORT):
        self._client = redis.Redis(host=host, port=port)
        self._pub_sub = self._client.pubsub(ignore_subscribe_messages=True)

    async def publish(self, channel: str, event: event.Event):
        self._client.publish(channel, json.dumps(asdict(event)))

    async def subscribe(self, channel: str):
        self._pub_sub.subscribe(channel)

    async def process(self, handle: Callable[..., Awaitable]):
        for message in self._pub_sub.listen():
            await handle(message)
