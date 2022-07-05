import abc
from typing import Optional, List
from uuid import uuid4

from atomos.core.domain.events import event


class EventQueue(abc.ABC):
    events: Optional[List[event.Event]] = []


class Model(EventQueue):
    id: Optional[str] = str(uuid4())
