from dataclasses import dataclass, field
from typing import Optional, List, Dict

from atomos.core.domain.commands import command
from identity.domain.model import role


@dataclass
class CreateUser(command.Command):
    username: str
    password: str
    email: str
    roles: Optional[List[role.Role]] = field(default_factory=lambda: [])


@dataclass
class UpdateUser(command.Command):
    username: Optional[str]
    email: Optional[str]
    update: Dict


@dataclass
class DeleteUser(command.Command):
    username: Optional[str]
    email: Optional[str]
