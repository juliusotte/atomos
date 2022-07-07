import grpc
from typing import List

from atomos.core.service.bus import message_bus

from identity.bootstrap import DEFAULT_BUS
from identity.api.proto import (
    identity_pb2 as identity_proto,
    identity_pb2_grpc as identity_grpc,
)
from identity.domain.commands import (
    permission_commands,
    role_commands,
    user_commands,
    api_key_commands,
)
from identity.domain.model import (
    permission as permission_model,
    role as role_model,
    user as user_model,
    api_key as api_key_model,
)
from identity.service.handlers import (
    permission_handlers,
    role_handlers,
    user_handlers,
    api_key_handlers,
)


class IdentityServicer(identity_grpc.IdentityServicer):
    def __init__(self):
        self.bus: message_bus.MessageBus = DEFAULT_BUS

    async def CreatePermission(
        self,
        request: identity_proto.CreatePermissionRequest,
        context,
    ) -> identity_proto.CreatePermissionResponse:
        if await permission_handlers.get_permission(request.permission, self.bus.uow):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('permission already exists under the provided name!')
            return
        await self.bus.handle(permission_commands.CreatePermission(request.permission))
        return identity_proto.CreatePermissionResponse()

    async def GetPermission(
        self,
        request: identity_proto.GetPermissionRequest,
        context,
    ) -> identity_proto.GetPermissionResponse:
        result = await permission_handlers.get_permission(request.permission, self.bus.uow)
        if not result:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('permission does not exist')
            return
        return identity_proto.GetPermissionResponse(identity_proto.Permission(result.permission))

    async def QueryPermissions(
        self,
        request: identity_proto.QueryPermissionsRequest,
        context,
    ) -> identity_proto.QueryPermissionsResponse:
        results = await permission_handlers.query_permissions({}, uow=self.bus.uow)
        if not results:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('no permissions found')
            return
        # map permission entities to proto DTO
        permissions: List[identity_proto.Permission] = list()
        for p in results:
            permissions.append(identity_proto.Permission(p.permission))
        return identity_proto.QueryPermissionsResponse(permissions)

    async def UpdatePermission(
        self,
        request: identity_proto.UpdatePermissionRequest,
        context,
    ) -> identity_proto.UpdatePermissionResponse:
        update = {
            'permission': request.update.permission,
        }
        await self.bus.handle(permission_commands.UpdatePermission(request.query.permission, update))
        return identity_proto.UpdatePermissionResponse()

    async def DeletePermission(
        self,
        request: identity_proto.DeletePermissionRequest,
        context,
    ) -> identity_proto.DeletePermissionResponse:
        if not await permission_handlers.get_permission(request.permission, self.bus.uow):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('permission does not exist')
            return
        await self.bus.handle(permission_commands.DeletePermission(request.permission))
        return identity_proto.DeletePermissionResponse()

    async def CreateRole(
        self,
        request: identity_proto.CreateRoleRequest,
        context,
    ) -> identity_proto.CreateRoleResponse:
        if await role_handlers.get_role(request.role, self.bus.uow):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('role already exists')
            return
        # map proto DTO to entity
        permissions: List[permission_model.Permission] = list()
        for p in request.permissions:
            permissions.append(permission_model.Permission(p.permission))
        await self.bus.handle(role_commands.CreateRole(request.role, permissions))
        return identity_proto.CreateRoleResponse()

    async def GetRole(
        self,
        request: identity_proto.GetRoleRequest,
        context,
    ) -> identity_proto.GetRoleResponse:
        result = await role_handlers.get_role(request.role, self.bus.uow)
        if not result:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('role does not exist')
            return
        # map permission entities to DTO
        permissions: List[identity_proto.Permission] = list()
        for p in result.permissions:
            permissions.append(identity_proto.Permission(p.permission))
        return identity_proto.GetRoleResponse(identity_proto.Role(result.role, permissions))

    async def QueryRoles(
        self,
        request: identity_proto.QueryRolesRequest,
        context,
    ) -> identity_proto.QueryRolesResponse:
        results = await role_handlers.query_roles({}, uow=self.bus.uow)
        if not results:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('no roles found')
            return
        # map roles entities to proto DTO
        roles: List[identity_proto.Role] = list()
        for r in results:
            permissions: List[identity_proto.Permission] = list()
            for p in r.permissions:
                permissions.append(identity_proto.Permission(p.permission))
            roles.append(identity_proto.Role(r.role, permissions))
        return identity_proto.QueryRolesRequest(roles)

    async def UpdateRole(
        self,
        request: identity_proto.UpdateRoleRequest,
        context,
    ) -> identity_proto.UpdateRoleResponse:
        # map update permissions DTO to domain entity
        permissions: List[permission_model.Permission] = list()
        for p in request.update.permissions:
            permissions.append(permission_model.Permission(p.permission))
        update = {
            'role': request.update.role,
            'permissions': permissions,
        }
        await self.bus.handle(role_commands.UpdateRole(request.query.role, **update))
        return identity_proto.UpdateRoleResponse()

    async def DeleteRole(
        self,
        request: identity_proto.DeleteRoleRequest,
        context,
    ) -> identity_proto.DeleteRoleResponse:
        if not role_handlers.get_role(request.role, self.bus.uow):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('role does not exist')
            return
        await self.bus.handle(role_commands.DeleteRole(request.role))
        return identity_proto.DeleteRoleResponse()

    async def CreateUser(
        self,
        request: identity_proto.CreateUserRequest,
        context,
    ) -> identity_proto.CreateUserResponse:
        if await user_handlers.get_user(request.username, request.email, self.bus.uow):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('user with specified username/email already exists')
            return
        # map proto DTO to roles entity
        roles: List[role_model.Role] = list()
        for r in request.roles:
            permissions: List[permission_model.Permission] = list()
            for p in r.permissions:
                permissions.append(permission_model.Permission(p.permission))
            roles.append(role_model.Role(r.role, permissions))
        await self.bus.handle(user_commands.CreateUser(request.username, request.password, request.email, roles))
        return identity_proto.CreateUserResponse()

    async def GetUser(
        self,
        request: identity_proto.GetUserRequest,
        context,
    ) -> identity_proto.GetUserResponse:
        result = await user_handlers.get_user(request.username, request.email, self.bus.uow)
        if not result:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('user does not exist')
            return
        # map roles entities to proto DTO
        roles: List[identity_proto.Role] = list()
        for r in result.roles:
            permissions: List[identity_proto.Permission] = list()
            for p in r.permissions:
                permissions.append(identity_proto.Permission(p.permission))
            roles.append(identity_proto.Role(r.role, permissions))
        return identity_proto.GetUserResponse(identity_proto.User(
            result.username,
            result.password,
            result.email,
            roles
        ))

    async def QueryUsers(
        self,
        request: identity_proto.QueryUsersResponse,
        context,
    ) -> identity_proto.QueryUsersResponse:
        results = await user_handlers.query_users({}, uow=self.bus.uow)
        if not results:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('no users found')
            return
        # map users entities to proto DTO
        users: List[identity_proto.User] = list()
        for u in results:
            roles: List[identity_proto.Role] = list()
            for r in roles:
                permissions: List[identity_proto.Permission] = list()
                for p in r.permissions:
                    permissions.append(identity_proto.Permission(p.permission))
                roles.append(identity_proto.Role(r.role, permissions))
            users.append(identity_proto.User(u.username, u.password, u.email, roles))
        return identity_proto.QueryUsersResponse(users)

    async def UpdateUser(
        self,
        request: identity_proto.UpdateUserRequest,
        context,
    ) -> identity_proto.UpdateUserResponse:
        roles: List[identity_proto.Role] = list()
        for r in request.update.roles:
            permissions: List[identity_proto.Permission] = list()
            for p in r.permissions:
                permissions.append(identity_proto.Permission(p.permission))
            roles.append(identity_proto.Role(r.role, permissions))
        update = {
            'username': request.update.username,
            'password': request.update.password,
            'email': request.update.password,
            'roles': roles,
        }
        await self.bus.handle(user_commands.UpdateUser(request.query.username, request.query.email, update))
        return identity_proto.UpdateUserResponse()

    async def DeleteUser(
        self,
        request: identity_proto.DeleteUserRequest,
        context,
    ) -> identity_proto.DeleteUserResponse:
        if not await user_handlers.get_user(request.username, request.email, self.bus.uow):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('user does not exist')
            return
        await self.bus.handle(user_commands.DeleteUser(request.username, request.email))
        return identity_proto.DeleteUserResponse()

    async def CreateAPIKey(
        self,
        request: identity_proto.CreateAPIKeyRequest,
        context,
    ) -> identity_proto.CreateAPIKeyResponse:
        # map proto DTO to user entity
        user: user_model.User = user_model.User(username=request.user.username, email=request.user.email)
        if await api_key_handlers.get_api_key(
            uow=self.bus.uow,
            user=user,
        ):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('API key with specified user already exists')
            return
        await self.bus.handle(api_key_commands.CreateAPIKey(user))
        return identity_proto.CreateAPIKeyResponse()

    async def GetAPIKey(
        self,
        request: identity_proto.GetAPIKeyRequest,
        context,
    ) -> identity_proto.GetAPIKeyResponse:
        user: user_model.User = user_model.User(username=request.user.username, email=request.user.email)
        key = request.key.uuid
        result = await api_key_handlers.get_api_key(uow=self.bus.uow, key=key, user=user)
        if not result:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('API key does not exist')
            return
        # map user entity to proto DTO
        user: identity_proto.User = identity_proto.User(username=result.user.username, email=result.user.email)
        return identity_proto.GetAPIKeyResponse(identity_proto.APIKey(
            result.key,
            user,
        ))

    async def UpdateAPIKey(
        self,
        request: identity_proto.UpdateAPIKeyRequest,
        context,
    ) -> identity_proto.UpdateAPIKeyResponse:
        user = user_model.User(username=request.update.user.username, email=request.update.user.email)
        query_key = request.query.key.uuid
        update_key = request.update.key.uuid
        update = {
            'user': user,
            'api_key': update_key,
        }
        await self.bus.handle(api_key_commands.UpdateAPIKey(api_key_model.APIKey(key=query_key), **update))
        return identity_proto.UpdateAPIKeyResponse()

    async def DeleteAPIKey(
        self,
        request: identity_proto.DeleteAPIKeyRequest,
        context,
    ) -> identity_proto.DeleteAPIKeyResponse:
        key = request.key.uuid
        if not await api_key_handlers.get_api_key(uow=self.bus.uow, key=key):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('API key does not exist')
            return
        await self.bus.handle(api_key_commands.DeleteAPIKey(key=key))
        return identity_proto.DeleteAPIKeyResponse()
