import abc
import uuid
from typing import Optional, List, Iterable

from atomos.core.adapters.repository import repository

from identity.domain.model import (
    permission as permission_model,
    role as role_model,
    user as user_model,
    api_key as api_key_model,
)


class IdentityRepository(repository.Repository):
    def __init__(self):
        super().__init__()

    async def create_permission(self, permission: str):
        await self._create_permission(permission)
        self.collected_entities.add(permission_model.Permission(permission=permission))

    async def get_permission(self, permission: str) -> Optional[permission_model.Permission]:
        result = await self._get_permission(permission)
        if result:
            self.collected_entities.add(result)
        return result

    async def query_permissions(self, **criterion) -> Iterable[permission_model.Permission]:
        results = await self._query_permissions(**criterion)
        if results:
            self.collected_entities.union(results)
        return results

    async def update_permission(self, permission: str, **update):
        await self._update_permission(permission, **update)

    async def delete_permission(self, permission: str):
        await self._delete_permission(permission)

    async def create_role(self, role: str, permissions: Optional[List[permission_model.Permission]]):
        await self._create_role(role, permissions)
        self.collected_entities.add(role_model.Role(role, permissions))

    async def get_role(self, role: str) -> Optional[role_model.Role]:
        result = await self._get_role(role)
        if result:
            self.collected_entities.add(result)
        return result

    async def query_roles(self, **criterion) -> Iterable[role_model.Role]:
        results = await self._query_roles(**criterion)
        if results:
            self.collected_entities.union(results)
        return results

    async def update_role(self, role: str, **update):
        await self._update_role(role, **update)

    async def delete_role(self, role: str):
        await self._delete_role(role)

    async def create_user(
        self,
        username: str,
        password: str,
        email: Optional[str],
        roles: Optional[List[role_model.Role]]
    ):
        await self._create_user(username, password, email, roles)
        self.collected_entities.add(user_model.User(username, password, email, roles))

    async def get_user(self, username: Optional[str] = None, email: Optional[str] = None) -> Optional[user_model.User]:
        result = await self._get_user(username=username, email=email)
        if result:
            self.collected_entities.add(result)
        return result

    async def query_users(self, **criterion) -> Iterable[user_model.User]:
        results = await self._query_users(**criterion)
        if results:
            self.collected_entities.union(results)
        return results

    async def update_user(self, username: Optional[str], email: Optional[str], **update):
        await self._update_user(username, email, **update)

    async def delete_user(self, username: Optional[str] = None, email: Optional[str] = None):
        await self._delete_user(username=username, email=email)

    async def create_api_key(self, user: user_model.User):
        await self._create_api_key(user)

    async def get_api_key(
        self,
        key: Optional[uuid.UUID],
        user: Optional[user_model.User],
    ) -> Optional[api_key_model.APIKey]:
        result = await self._get_api_key(key=key, user=user)
        if result:
            self.collected_entities.add(result)
        return result

    async def update_api_key(self, api_key: api_key_model.APIKey, **update):
        await self._update_api_key(api_key, **update)

    async def delete_api_key(self, api_key: api_key_model.APIKey):
        await self._delete_api_key(api_key)

    @abc.abstractmethod
    async def _create_permission(self, permission: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_permission(self, permission: str) -> Optional[permission_model.Permission]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _query_permissions(self, **criterion) -> Iterable[permission_model.Permission]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update_permission(self, permission: str, **update):
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete_permission(self, permission: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def _create_role(self, role: str, permissions: Optional[List[permission_model.Permission]]):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_role(self, role: str) -> Optional[role_model.Role]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _query_roles(self, **criterion) -> Iterable[role_model.Role]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update_role(self, role: str, **update):
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete_role(self, role: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def _create_user(
        self,
        username: str,
        password: str,
        email: Optional[str],
        roles: Optional[List[role_model.Role]]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_user(self, username: Optional[str], email: Optional[str]) -> Optional[user_model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _query_users(self, **criterion) -> Iterable[user_model.User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update_user(self, username: Optional[str], email: Optional[str], **update):
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete_user(self, **criterion):
        raise NotImplementedError

    @abc.abstractmethod
    async def _create_api_key(self, user: user_model.User):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_api_key(self, **criterion) -> Optional[api_key_model.APIKey]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update_api_key(self, api_key: api_key_model.APIKey, **update):
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete_api_key(self, api_key: api_key_model.APIKey):
        raise NotImplementedError
