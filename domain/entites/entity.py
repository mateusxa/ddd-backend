

from datetime import datetime, timezone


class EntityId:
    value: str


    def __init__(self, value: str | None):
        self.value = value or ""

    
    def __str__(self):
        return self.value
    

    def get_class_name(self):
        return _get_plural_name(self.__class__.__name__.lower()[:-2])


class Entity:
    id: EntityId
    
    def to_dict(self):
        return vars(self)
    
    
    def get_class_name(self):
        return _get_plural_name(self.__class__.__name__.lower())


def _get_plural_name(name: str):
    return name + "s" if name[-1] != "y" else name[:-1] + "ies"
