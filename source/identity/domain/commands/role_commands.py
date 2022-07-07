from dataclasses import dataclass, field
from typing import Optional, List, Dict

from atomos.core.domain.commands import command
from identity.domain.model import permission


@dataclass
class CreateRole(command.Command):
    role: str
    permissions: Optional[List[permission.Permission]] = field(default_factory=lambda: [])


@dataclass
class UpdateRole(command.Command):
    role: str
    update: Dict


@dataclass
class DeleteRole(command.Command):
    role: str
