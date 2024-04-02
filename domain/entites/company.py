from datetime import datetime, timezone
from domain.entites.entity import Entity


class Company(Entity):
    
    name: str
    tax_id: str
    id: str | None
    created: datetime

    def __init__(self, name: str, tax_id: str, id: str | None = None, created: datetime | None = None):
        self.name = name
        self.tax_id = tax_id
        self.id = id
        self.created = created or datetime.now(timezone.utc)


    def __repr__(self):
        return f"Company(\
            name={self.name}, \
            tax_id={self.tax_id}, \
            id={self.id}, \
            created={self.created}\
        )"


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Company.__annotations__):
            raise Exception(f"dict incomplete! {source}")
        return Company(
            name = source["name"],
            tax_id = source["tax_id"],
            id = source["id"],
            created = source["created"],
        )
