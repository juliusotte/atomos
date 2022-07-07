import uuid
from dataclasses import dataclass, field
from typing import Optional, List

from atomos.core.domain.model import model
from identity.domain.model import role


@dataclass
class User(model.Model):
    username: str
    password: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[List[role.Role]] = field(default_factory=lambda: [])
    id: Optional[uuid.UUID] = uuid.uuid4()

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other):
        return isinstance(other, User) and self.id is other.id
