import uuid
from typing import Optional

from atomos.core.adapters.notification import notification
from atomos.core.adapters.messaging import message_broker
from atomos.core.service.uow import unit_of_work

from identity.domain.model import (
    api_key as api_key_model,
    user as user_model,
)
from identity.domain.commands import api_key_commands as commands
from identity.domain.events import api_key_events as events
from identity.adapters.repository.repository import IdentityRepository


async def get_api_key(
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    key: Optional[uuid.UUID] = None,
    user: Optional[user_model.User] = None,
) -> Optional[api_key_model.APIKey]:
    async with uow:
        result = await uow.repository.get_api_key(key, user)
    return result


async def create_api_key(
    c: commands.CreateAPIKey,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    if not await get_api_key(uow, user=c.user):
        async with uow:
            await uow.repository.create_api_key(c.user)
            await uow.commit()
        api_key: api_key_model.APIKey = await get_api_key(uow, user=c.user)
        await broker.publish('api_key_created', events.APIKeyCreated(user=c.user, key=api_key.key))


async def update_api_key(
    c: commands.UpdateAPIKey,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        await uow.repository.update_api_key(c.query, **c.update)
        await uow.commit()
    await broker.publish('api_key_updated', events.APIKeyUpdated(c.query.key, **c.update))


async def delete_api_key(
    c: commands.DeleteAPIKey,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    broker: message_broker.MessageBroker,
):
    async with uow:
        api_key: api_key_model.APIKey = await get_api_key(uow, key=c.key)
        await uow.repository.delete_api_key(api_key_model.APIKey(key=c.key))
        await uow.commit()
    await broker.publish('api_key_deleted', events.APIKeyDeleted(key=api_key.key, user=api_key.user))


async def notify_admin_api_key_created(
    e: events.APIKeyCreated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: API Key Creation\n'
        f'User: {e.user.username}\n'
        f'E-Mail: {e.user.email}\n'
        f'Roles: {e.user.roles}\n'
        f'API Key: {e.key}\n'
    )


async def notify_admin_api_key_updated(
    e: events.APIKeyUpdated,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: API Key Update\n'
        f'API Key: {e.key}\n'
        f'Update: {e.update}\n'
    )


async def notify_admin_api_key_deleted(
    e: events.APIKeyDeleted,
    notification: notification.Notification,
):
    await notification.notify(
        'admin@domain.tld',
        'Event: API Key Deletion\n'
        f'API Key: {e.key}\n'
        f'Username: {e.user.username}'
        f'E-Mail: {e.user.email}'
        f'Roles: {e.user.roles}'
    )


async def api_key_created_notification(
    e: events.APIKeyCreated,
    notification: notification.Notification,
):
    await notification.notify(
        e.user.email,
        f'''
        API Key Creation Confirmation
        '''
    )


async def api_key_updated_notification(
    e: events.APIKeyUpdated,
    uow: unit_of_work.UnitOfWork[IdentityRepository],
    notification: notification.Notification,
):
    with uow:
        api_key: api_key_model.APIKey = await get_api_key(uow, key=e.key)
    await notification.notify(
        api_key.user.email,
        f'''
        API Key Update Confirmation
        '''
    )


async def api_key_deleted_notification(
    e: events.APIKeyDeleted,
    notification: notification.Notification,
):
    await notification.notify(
        e.user.email,
        f'''
        API Key Deletion Confirmation
        '''
    )
