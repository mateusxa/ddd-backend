from datetime import datetime, timezone
from domain.entites import Entity
from utils.error import Error


class Report(Entity):

    def __init__(
            self, company_id: str, name: str, bucket_url: str | None = None, 
            id: str | None = None, created: datetime | None = None
        ):
        self._company_id = company_id
        self._name = name
        self._bucket_url = bucket_url
        self._id = id
        self._created = created or datetime.now(timezone.utc)


    @property
    def name(self) -> str:
        return  self._name
    
    @property
    def company_id(self) -> str:
        return  self._company_id
    
    @property
    def bucket_url(self) -> str | None:
        return  self._bucket_url
    
    @bucket_url.setter
    def bucket_url(self, bucket_url: str):
        self._bucket_url = bucket_url
    
    @property
    def id(self) -> str | None:
        return  self._id
    
    @property
    def created(self) -> datetime:
        return  self._created

    def __repr__(self):
        return f"Report(\
            company_id={self.company_id}, \
            name={self.name}, \
            bucket_url={self.bucket_url}, \
            id={self.id}, \
            created={self.created}\
        )"

    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Report.__annotations__):
            raise Error(Error.Code.internal_error, str(source), 500)
        return Report(
            id = source["id"],
            company_id = source["company_id"],
            name = source["name"],
            bucket_url = source["bucket_url"],
            created = source["created"],
        )
    