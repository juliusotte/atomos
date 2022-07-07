from dataclasses import dataclass
import uuid
from typing import Dict

from atomos.core.domain.events import event
from identity.domain.model import user


@dataclass
class APIKeyCreated(event.Event):
    key: uuid.UUID
    user: user.User


@dataclass
class APIKeyUpdated(event.Event):
    key: uuid.UUID
    update: Dict


@dataclass
class APIKeyDeleted(event.Event):
    key: uuid.UUID
    user: user.User
