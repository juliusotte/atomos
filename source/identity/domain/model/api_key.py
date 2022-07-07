from dataclasses import dataclass
import uuid

from atomos.core.domain.model import model


@dataclass
class APIKey(model.Model):
    user_id: uuid.UUID
    key: uuid.UUID = uuid.uuid4()

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return isinstance(other, APIKey) \
               and self.key is other.key \
               and self.user_id is other.user_id
