import inspect
import logging
import asyncio

from atomos.core.adapters.messaging import message_broker, redis_pub_sub_broker
from atomos.core.adapters.notification import notification, email
from atomos.core.service.bus import message_bus
from atomos.core.service.uow import unit_of_work

from identity.adapters.orm import orm, defaults
from identity.service.handlers import handlers
from identity.service.uow.sqlalchemy_unit_of_work import SQLAlchemyIdentityUnitOfWork
from identity.adapters.repository.sqlalchemy_repository import SQLAlchemyIdentityRepository


async def bootstrap(
    init_orm: bool = True,
    uow: unit_of_work.UnitOfWork[SQLAlchemyIdentityRepository] = SQLAlchemyIdentityUnitOfWork(),
    broker: message_broker.MessageBroker = redis_pub_sub_broker.RedisPubSubBroker(),
    notifications: notification.Notification = email.EMailNotification(),
) -> message_bus.MessageBus:

    dependencies = {
        'uow': uow,
        'broker': broker,
        'notification': notifications,
    }

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    bus = message_bus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

    if init_orm:
        orm.init_orm()
        await defaults.create_defaults(bus)

    return bus


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)


DEFAULT_BUS: message_bus.MessageBus = asyncio.run(bootstrap())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    bootstrap()
