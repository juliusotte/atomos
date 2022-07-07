from dataclasses import dataclass
from typing import Dict

from atomos.core.domain.events import event


@dataclass
class PermissionCreated(event.Event):
    permission: str


@dataclass
class PermissionUpdated(event.Event):
    permission: str
    update: Dict


@dataclass
class PermissionDeleted(event.Event):
    permission: str
