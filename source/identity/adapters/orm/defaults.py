import logging

from atomos.core.service.bus import message_bus

from identity.domain.model import role
from identity.service.handlers import role_handlers
from identity.domain.commands import role_commands

logger = logging.getLogger(__name__)


async def create_defaults(bus: message_bus.MessageBus):
    logger.info('creating system defaults in ORM')

    # Roles
    logger.info('creating default roles')
    for default in role.Roles:
        logger.info('creating default role: %s', default.value)

        # Check if role already exists
        result = await role_handlers.get_role(default.value, bus.uow)
        if result:
            logger.info('role %s already exists, skipping creation', default.value)
            continue

        await bus.handle(role_commands.CreateRole(default.value, []))
