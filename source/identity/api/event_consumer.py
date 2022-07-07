import json
import logging
import asyncio
from typing import Dict, Type

from atomos.core.adapters.messaging import redis_pub_sub_broker
from atomos.core.domain.events import event

from identity.bootstrap import DEFAULT_BUS
from identity.domain.events import (
    permission_events,
    role_events,
    user_events,
)

logger = logging.getLogger(__name__)


CHANNELS = {
    'permission_created': permission_events.PermissionCreated,
    'permission_updated': permission_events.PermissionUpdated,
    'permission_deleted': permission_events.PermissionDeleted,

    'role_created': role_events.RoleCreated,
    'role_updated': role_events.RoleUpdated,
    'role_deleted': role_events.RoleDeleted,

    'user_created': user_events.UserCreated,
    'user_updated': user_events.UserUpdated,
    'user_deleted': user_events.UserDeleted,
}


def inject_dependencies(message: Type, data: Dict) -> event.Event:
    m: event.Event = message(**data)
    return m


async def main():
    logger.info('initializing redis pub/sub broker')
    broker = redis_pub_sub_broker.RedisPubSubBroker()

    # Subscribe to registered channels
    for channel in CHANNELS.keys():
        await broker.subscribe(channel)

    # Listening and handling incoming messages
    await broker.process(handle)


async def handle(message: dict):
    logger.info('handling %s', message)
    data = json.loads(message['data'])
    channel = message['channel'].decode('utf-8')

    # Inject raw data into an event that is determined by the channel name
    injected_event_message = inject_dependencies(CHANNELS.get(channel), data)

    # Handle injected message (payload) with the message bus
    await DEFAULT_BUS.handle(injected_event_message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
