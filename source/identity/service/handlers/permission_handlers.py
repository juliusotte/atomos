from typing import Optional, Dict, Iterable

from atomos.core.adapters.notification import notification
from atomos.core.adapters.messaging import message_broker
from atomos.core.service.uow import unit_of_work

from identity.domain.model import permission as model
from identity.domain.commands import permission_commands as commands
from identity.domain.events import permission_events as events
from identity.adapters.repository.repository import IdentityRepository


async def get_permission(
    permission: str,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
) -> Optional[model.Permission]:
    async with uow:
        result = await uow.repository.get_permission(permission)
    return result


async def query_permissions(
    criterion: Dict,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
) -> Optional[Iterable[model.Permission]]:
    async with uow:
        results = await uow.repository.query_permissions(**criterion)
    return results


async def create_permission(
    c: commands.CreatePermission,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    if not await get_permission(c.permission, uow):
        async with uow:
            await uow.repository.create_permission(c.permission)
            await uow.commit()
        await broker.publish('permission_created', events.PermissionCreated(c.permission))


async def update_permission(
    c: commands.UpdatePermission,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.update_permission(c.permission, **c.update)
        await uow.commit()
    await broker.publish('permission_updated', events.PermissionUpdated(c.permission, c.update))


async def delete_permission(
    c: commands.DeletePermission,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.delete_permission(c.permission)
        await uow.commit()
    await broker.publish('permission_deleted', events.PermissionDeleted(c.permission))


async def notify_admin_permission_created(
    e: events.PermissionCreated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: Permission Creation\n'
        f'Permission: {e.permission}\n'
    )


async def notify_admin_permission_updated(
    e: events.PermissionUpdated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: Permission Update\n'
        f'Permission: {e.permission}\n'
        f'Update: {e.update}\n'
    )


async def notify_admin_permission_deleted(
    e: events.PermissionDeleted,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: Permission Deletion\n'
        f'Permission: {e.permission}\n'
    )
