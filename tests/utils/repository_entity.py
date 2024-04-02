from datetime import datetime, timezone
from domain.entites.entity import Entity


class TestRepository(Entity):
    __test__ = False
    name: str
    id: str | None
    created: datetime | None


    def __init__(self, name: str, id: str | None = None, created: datetime | None = None):
        self.id = id
        self.name = name
        self.created = created or datetime.now(timezone.utc)


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in TestRepository.__annotations__):
            raise Exception(f"dict incomplete! {source}")
        return TestRepository(
            id = str(source["id"]),
            name = source["name"],
            created = source["created"],
        )
    
    def __repr__(self):
        return f"TestRepository(\
            name={self.name}, \
            id={self.id}, \
            created={self.created}, \
        )"