import logging
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.engine import Engine

from atomos.core.adapters.orm import factory

from identity.domain.model import (
    permission,
    role,
    user,
    api_key,
)

logger = logging.getLogger(__name__)

meta = MetaData()

permissions_table = Table(
    'permissions',
    meta,
    Column('permission', String, primary_key=True),
)

roles_table = Table(
    'roles',
    meta,
    Column('role', String, primary_key=True),
    Column('permissions', JSON, nullable=False),
)

users_table = Table(
    'users',
    meta,
    Column('id', String, primary_key=True),
    Column('username', String, nullable=True),
    Column('password', String, nullable=False),
    Column('email', String, nullable=False),
    Column('roles', JSON, nullable=False),
)

api_keys_table = Table(
    'api_keys',
    meta,
    Column('key', String, primary_key=True),
    Column('user_id', ForeignKey('users.id')),
)

mapping_permissions = mapper(permission.Permission, permissions_table)
mapping_roles = mapper(role.Role, roles_table)
mapping_api_keys = mapper(api_key.APIKey, api_keys_table)
mapping_users = mapper(user.User, users_table, properties={
    'api_keys': relationship(mapping_api_keys),
})


def init_orm(engine: Engine = factory.DEFAULT_ENGINE):
    logger.info('initializing ORM')

    meta.create_all(engine, checkfirst=True)
