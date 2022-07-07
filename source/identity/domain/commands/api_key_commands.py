from dataclasses import dataclass
import uuid
from typing import Dict

from atomos.core.domain.commands import command
from identity.domain.model import user, api_key


@dataclass
class CreateAPIKey(command.Command):
    user: user.User


@dataclass
class UpdateAPIKey(command.Command):
    query: api_key.APIKey
    update: Dict


@dataclass
class DeleteAPIKey(command.Command):
    key: uuid.UUID
