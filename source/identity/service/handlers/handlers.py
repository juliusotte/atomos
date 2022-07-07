from typing import Type, Dict, List, Callable, Union, Awaitable

from algoid.core.domain.events import event

from identity.domain.events import (
    permission_events,
    role_events,
    user_events,
    api_key_events,
)

from algoid.core.domain.commands import command

from identity.domain.commands import (
    permission_commands,
    role_commands,
    user_commands,
    api_key_commands,
)

from identity.service.handlers import (
    permission_handlers,
    role_handlers,
    user_handlers,
    api_key_handlers,
)

EVENT_HANDLERS: Dict[Type[event.Event], List[Callable[..., Union[Awaitable, None]]]] = {
    permission_events.PermissionCreated: [permission_handlers.notify_admin_permission_created],
    permission_events.PermissionUpdated: [permission_handlers.notify_admin_permission_updated],
    permission_events.PermissionDeleted: [permission_handlers.notify_admin_permission_deleted],
    role_events.RoleCreated: [role_handlers.notify_admin_role_created],
    role_events.RoleUpdated: [role_handlers.notify_admin_role_updated],
    role_events.RoleDeleted: [role_handlers.notify_admin_role_deleted],
    user_events.UserCreated: [user_handlers.user_created_notification, user_handlers.notify_admin_user_created],
    user_events.UserUpdated: [user_handlers.user_updated_notification, user_handlers.notify_admin_user_updated],
    user_events.UserDeleted: [user_handlers.user_deleted_notification, user_handlers.notify_admin_user_deleted],
    api_key_events.APIKeyCreated: [api_key_handlers.api_key_created_notification, api_key_handlers.notify_admin_api_key_created],
    api_key_events.APIKeyUpdated: [api_key_handlers.api_key_updated_notification, api_key_handlers.notify_admin_api_key_updated],
    api_key_events.APIKeyDeleted: [api_key_handlers.api_key_deleted_notification, api_key_handlers.notify_admin_api_key_deleted],
}

COMMAND_HANDLERS: Dict[Type[command.Command], Callable[..., Union[Awaitable, None]]] = {
    permission_commands.CreatePermission: permission_handlers.create_permission,
    permission_commands.UpdatePermission: permission_handlers.update_permission,
    permission_commands.DeletePermission: permission_handlers.delete_permission,
    role_commands.CreateRole: role_handlers.create_role,
    role_commands.UpdateRole: role_handlers.update_role,
    role_commands.DeleteRole: role_handlers.delete_role,
    user_commands.CreateUser: user_handlers.create_user,
    user_commands.UpdateUser: user_handlers.update_user,
    user_commands.DeleteUser: user_handlers.delete_user,
    api_key_commands.CreateAPIKey: api_key_handlers.create_api_key,
    api_key_commands.UpdateAPIKey: api_key_handlers.update_api_key,
    api_key_commands.DeleteAPIKey: api_key_handlers.delete_api_key,
}
