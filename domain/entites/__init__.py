from abc import ABC, abstractmethod
from datetime import datetime


class Entity(ABC):

    @property
    @abstractmethod
    def id(self) -> str | None:
        pass

    @property
    @abstractmethod
    def created(self) -> datetime | None:
        pass

    def to_dict(self):
        dict_data = vars(self)
        return {key.lstrip('_'): value for key, value in dict_data.items()}
    
    @staticmethod
    @abstractmethod
    def from_dict(entity_dict: dict):
        pass
