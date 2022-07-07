from dataclasses import dataclass
from typing import Dict

from atomos.core.domain.commands import command


@dataclass
class CreatePermission(command.Command):
    permission: str


@dataclass
class UpdatePermission(command.Command):
    permission: str
    update: Dict


@dataclass
class DeletePermission(command.Command):
    permission: str
