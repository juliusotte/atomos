from dataclasses import dataclass, field
from typing import Optional, Dict, List

from atomos.core.domain.events import event
from identity.domain.model import role


@dataclass
class UserCreated(event.Event):
    username: Optional[str]
    email: Optional[str]
    roles: Optional[List[role.Role]] = field(default_factory=lambda: [])


@dataclass
class UserUpdated(event.Event):
    username: Optional[str]
    email: Optional[str]
    update: Dict


@dataclass
class UserDeleted(event.Event):
    username: Optional[str]
    email: Optional[str]
