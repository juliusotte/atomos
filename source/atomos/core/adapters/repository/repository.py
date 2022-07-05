import abc
from typing import Set

from atomos.core.domain.model import model


class Repository(abc.ABC):
    collected_entities: Set[model.Model]

    def __init__(self):
        self.collected_entities = set()
