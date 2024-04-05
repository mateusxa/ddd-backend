from datetime import datetime, timezone
from domain.entites import Entity
from utils.error import Error


class Company(Entity):
    
    def __init__(self, name: str, tax_id: str, id: str | None = None, created: datetime | None = None):
        self._name = name
        self._tax_id = tax_id
        self._id = id
        self._created = created or datetime.now(timezone.utc)

    @property
    def name(self) -> str:
        return  self._name
    
    @property
    def tax_id(self) -> str:
        return  self._tax_id
    
    @property
    def id(self) -> str | None:
        return  self._id
    
    @property
    def created(self) -> datetime:
        return  self._created

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
            raise Error(Error.Code.internal_error, str(source), 500)
        return Company(
            name = source["name"],
            tax_id = source["tax_id"],
            id = source["id"],
            created = source["created"],
        )
