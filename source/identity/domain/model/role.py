import enum
from dataclasses import dataclass, field
from typing import Optional, List

from atomos.core.domain.model import model
from identity.domain.model import permission


class Roles(enum.Enum):
    USER = 'user'
    SUPPORTER = 'supporter'
    MODERATOR = 'moderator'
    DEVELOPER = 'developer'
    ADMINISTRATOR = 'administrator'


@dataclass
class Role(model.Model):
    role: str
    permissions: Optional[List[permission.Permission]] = field(default_factory=lambda: [])

    def __hash__(self):
        return hash(self.role)

    def __eq__(self, other):
        return isinstance(other, Role) and self.role is other.role
