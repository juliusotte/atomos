import logging
import grpc
import asyncio
from typing import Optional, List

from atomos.core import config
from identity.api.proto import identity_pb2, identity_pb2_grpc

from identity.domain.model import role, permission


async def create_permission(
    stub: identity_pb2_grpc.IdentityStub,
    permission: str,
):
    await stub.CreatePermission(identity_pb2.CreatePermissionRequest(permission=permission))


async def delete_permission(
    stub: identity_pb2_grpc.IdentityStub,
    permission: str,
):
    await stub.DeletePermission(identity_pb2.DeletePermissionRequest(permission=permission))


async def create_role(
    stub: identity_pb2_grpc.IdentityStub,
    role: str,
    permissions: List[permission.Permission],
):
    mapped_permissions: List[identity_pb2.Permission] = list()
    for p in permissions:
        mapped_permissions.append(identity_pb2.Permission(permission=p.permission))
    await stub.CreateRole(identity_pb2.CreateRoleRequest(role=role, permissions=mapped_permissions))


async def delete_role(
    stub: identity_pb2_grpc.IdentityStub,
    role: str,
):
    await stub.DeleteRole(identity_pb2.DeleteRoleRequest(role=role))


async def create_user(
    stub: identity_pb2_grpc.IdentityStub,
    username: str,
    password: str,
    email: str,
    roles: Optional[List[role.Role]] = None,
):
    mapped_roles: List[identity_pb2.Role] = list()
    if roles is not None:
        for r in roles:
            permissions: List[identity_pb2.Permission] = list()
            for p in r.permissions:
                permissions.append(identity_pb2.Permission(p.permission))
            mapped_roles.append(identity_pb2.Role(r.role, permissions))
    request = identity_pb2.CreateUserRequest(username=username, password=password, email=email, roles=mapped_roles)
    await stub.CreateUser(request)


async def delete_user(
    stub: identity_pb2_grpc.IdentityStub,
    username: Optional[str] = None,
    email: Optional[str] = None,
):
    await stub.DeleteUser(identity_pb2.DeleteUserRequest(username=username, email=email))


async def main():
    async with grpc.aio.insecure_channel(f'{config.API_HOST}:{config.API_PORT}') as channel:
        stub = identity_pb2_grpc.IdentityStub(channel)

        # CREATE
        await create_permission(stub, 'test')
        await create_role(stub, 'admin', [permission.Permission('admin')])
        await create_user(stub, 'john.doe', 'secret', 'john.doe@johndoe.com', [])

        # DELETE
        await delete_permission(stub, 'test')
        await delete_role(stub, 'admin')
        await delete_user(stub, 'john.doe', 'john.doe@johndoe.com')

if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(main())
