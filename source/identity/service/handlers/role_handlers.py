from typing import Optional, Dict, Iterable

from atomos.core.adapters.notification import notification
from atomos.core.adapters.messaging import message_broker
from atomos.core.service.uow import unit_of_work

from identity.domain.model import role as model
from identity.domain.commands import role_commands as commands
from identity.domain.events import role_events as events
from identity.adapters.repository.repository import IdentityRepository


async def get_role(
    role: str,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
) -> Optional[model.Role]:
    async with uow:
        result = await uow.repository.get_role(role)
    return result


async def query_roles(
    criterion: Dict,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
) -> Optional[Iterable[model.Role]]:
    async with uow:
        results = await uow.repository.query_roles(**criterion)
    return results


async def create_role(
    c: commands.CreateRole,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    if not await get_role(c.role, uow):
        async with uow:
            await uow.repository.create_role(c.role, c.permissions)
            await uow.commit()
        await broker.publish('role_created', events.RoleCreated(c.role, c.permissions))


async def update_role(
    c: commands.UpdateRole,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.update_role(c.role, **c.update)
        await uow.commit()
    await broker.publish('role_updated', events.RoleUpdated(c.role, c.update))


async def delete_role(
    c: commands.DeleteRole,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.delete_role(c.role)
        await uow.commit()
    await broker.publish('role_deleted', events.RoleDeleted(c.role))


async def notify_admin_role_created(
    e: events.RoleCreated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: Role Creation\n'
        f'Role: {e.role}\n'
        f'Permissions: {e.permissions}\n'
    )


async def notify_admin_role_updated(
    e: events.RoleUpdated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: Role Update\n'
        f'Role: {e.role}\n'
        f'Update: {e.update}\n'
    )


async def notify_admin_role_deleted(
    e: events.RoleDeleted,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: Role Deletion\n'
        f'Role: {e.role}\n'
    )
