from dataclasses import dataclass

from atomos.core.domain.model import model


@dataclass
class Permission(model.Model):
    permission: str

    def __hash__(self):
        return hash(self.permission)

    def __eq__(self, other):
        return isinstance(other, Permission) and self.permission is other.permission
