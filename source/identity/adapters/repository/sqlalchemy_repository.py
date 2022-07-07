import abc
from typing import Optional, Iterable, List
from sqlalchemy.orm import Session

from atomos.core.adapters.repository import sqlalchemy_repository
from atomos.core.adapters.orm import factory

from identity.adapters.repository import repository
from identity.domain.model import (
    user as user_model,
    role as role_model,
    permission as permission_model,
    api_key as api_key_model,
)


class SQLAlchemyIdentityRepository(
    sqlalchemy_repository.SQLAlchemyRepository,
    repository.IdentityRepository
):
    def __init__(self, session: Session = factory.DEFAULT_SESSION_FACTORY()):
        super().__init__(session)
        self.session = session

    async def _create_permission(self, permission: str):
        if not await self._get_permission(permission):
            self.session.add(permission_model.Permission(permission))

    async def _get_permission(self, permission: str) -> Optional[permission_model.Permission]:
        return self.session.query(permission_model.Permission).filter_by(permission=permission).first()

    async def _query_permissions(self, **criterion) -> Iterable[permission_model.Permission]:
        return self.session.query(permission_model.Permission).filter_by(**criterion).all()

    async def _update_permission(self, permission: str, **update):
        self.session.query(permission_model.Permission).filter_by(permission=permission).update(**update)

    async def _delete_permission(self, permission: str):
        result = await self._get_permission(permission)
        if result:
            self.session.delete(result)

    async def _create_role(self, role: str, permissions: Optional[List[permission_model.Permission]]):
        if not await self._get_role(role):
            self.session.add(role_model.Role(role, permissions))

    async def _get_role(self, role: str) -> Optional[role_model.Role]:
        return self.session.query(role_model.Role).filter_by(role=role).first()

    async def _query_roles(self, **criterion) -> Iterable[role_model.Role]:
        return self.session.query(role_model.Role).filter_by(**criterion).all()

    async def _update_role(self, role: str, **update):
        self.session.query(role_model.Role).filter_by(role=role).update(**update)

    async def _delete_role(self, role: str):
        result = await self._get_role(role)
        if result:
            self.session.delete(result)

    async def _create_user(
        self,
        username: str,
        password: str,
        email: Optional[str],
        roles: Optional[List[role_model.Role]]
    ):
        if not await self._get_user(username=username, email=email):
            self.session.add(user_model.User(username, password, email, roles))

    async def _get_user(self, **criterion) -> Optional[user_model.User]:
        data = {
            k: v
            for k, v in criterion.items()
            if k in ['username', 'email']
            and v is not None
        }
        if not data:
            return None
        return self.session.query(user_model.User).filter_by(**data).first()

    async def _query_users(self, **criterion) -> Iterable[user_model.User]:
        return self.session.query(user_model.User).filter_by(**criterion).all()

    async def _update_user(self, username: Optional[str], email: Optional[str], **update):
        self.session.query(user_model.User).filter_by(username=username, email=email).update(**update)

    async def _delete_user(self, **criterion):
        result = await self._get_user(**criterion)
        if result:
            self.session.delete(result)

    async def _create_api_key(self, user: user_model.User):
        if not await self._get_api_key(user=user):
            self.session.add(api_key_model.APIKey(user=user))

    async def _get_api_key(self, **criterion) -> Optional[api_key_model.APIKey]:
        return self.session.query(api_key_model.APIKey).filter_by(**criterion).first()

    async def _update_api_key(self, api_key: api_key_model.APIKey, **update):
        self.session.query(api_key_model.APIKey).filter_by(key=api_key.key, user_id=api_key.user_id).update(**update)

    async def _delete_api_key(self, api_key: api_key_model.APIKey):
        result = self._get_api_key(key=api_key.key, user_id=api_key.user_id)
        if result:
            self.session.delete(result)
