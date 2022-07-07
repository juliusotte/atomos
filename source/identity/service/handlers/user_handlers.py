from typing import Optional, Dict, Iterable

from atomos.core.adapters.notification import notification
from atomos.core.adapters.messaging import message_broker
from atomos.core.service.uow import unit_of_work

from identity.domain.model import user as model
from identity.domain.commands import user_commands as commands
from identity.domain.events import user_events as events
from identity.adapters.repository.repository import IdentityRepository


async def get_user(
    username: Optional[str],
    email: Optional[str],
    uow: unit_of_work.UnitOfWork[IdentityRepository],
) -> Optional[model.User]:
    async with uow:
        result = await uow.repository.get_user(username, email)
    return result


async def query_users(
    criterion: Dict,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
) -> Optional[Iterable[model.User]]:
    async with uow:
        results = await uow.repository.query_users(**criterion)
    return results


async def create_user(
    c: commands.CreateUser,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    if not await get_user(c.username, c.email, uow):
        async with uow:
            await uow.repository.create_user(c.username, c.password, c.email, c.roles)
            await uow.commit()
        await broker.publish('user_created', events.UserCreated(c.username, c.username, c.roles))


async def update_user(
    c: commands.UpdateUser,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.update_user(c.username, c.email, **c.update)
        await uow.commit()
    await broker.publish('user_updated', events.UserUpdated(c.username, c.email, **c.update))


async def delete_user(
    c: commands.DeleteUser,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.delete_user(c.username, c.email)
        await uow.commit()
    await broker.publish('user_deleted', events.UserDeleted(c.username, c.email))


async def notify_admin_user_created(
    e: events.UserCreated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: User Creation\n'
        f'Username: {e.username}\n'
        f'E-Mail: {e.email}\n'
        f'Roles: {e.roles}\n'
    )


async def notify_admin_user_updated(
    e: events.UserUpdated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: User Update\n'
        f'Username: {e.username}\n'
        f'E-Mail: {e.email}\n'
        f'Update: {e.update}\n'
    )


async def notify_admin_user_deleted(
    e: events.UserDeleted,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: User Deletion\n'
        f'Username: {e.username}\n'
        f'E-Mail: {e.email}\n'
    )


async def user_created_notification(
    e: events.UserCreated,
    notification: notification.Notification,
):
    await notification.notify(
        e.email,
        f'''
        Registration Confirmation
        '''
    )


async def user_updated_notification(
    e: events.UserUpdated,
    notification: notification.Notification,
):
    await notification.notify(
        e.email,
        f'''
        Update Confirmation
        '''
    )


async def user_deleted_notification(
    e: events.UserDeleted,
    notification: notification.Notification,
):
    await notification.notify(
        e.email,
        f'''
        Account Deletion Confirmation
        '''
    )
