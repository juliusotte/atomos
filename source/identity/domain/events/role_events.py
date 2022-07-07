from dataclasses import dataclass, field
from typing import Dict, List, Optional

from atomos.core.domain.events import event
from identity.domain.model import permission


@dataclass
class RoleCreated(event.Event):
    role: str
    permissions: Optional[List[permission.Permission]] = field(default_factory=lambda: [])


@dataclass
class RoleUpdated(event.Event):
    role: str
    update: Dict


@dataclass
class RoleDeleted(event.Event):
    role: str
