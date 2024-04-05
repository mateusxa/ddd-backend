from abc import ABC, abstractmethod
from domain.entites import Entity


class Repository(ABC):

    @abstractmethod
    def create(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Entity | None:
        pass

    @abstractmethod
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs)-> tuple[str | None, list[Entity]]:
        pass

    @abstractmethod
    def update(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    def delete(self, entity: Entity) -> None:
        pass
