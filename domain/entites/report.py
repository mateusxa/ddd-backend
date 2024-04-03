from datetime import datetime, timezone
from domain.entites import Entity
from utils.error import DictIncomplete


class Report(Entity):

    company_id: str
    name: str
    bucket_url: str | None
    id: str | None
    created: datetime


    def __init__(
            self, company_id: str, name: str, bucket_url: str | None = None, 
            id: str | None = None, created: datetime | None = None
        ):
        self.company_id = company_id
        self.name = name
        self.bucket_url = bucket_url
        self.id = id
        self.created = created or datetime.now(timezone.utc)


    def __repr__(self):
        return f"Report(\
            company_id={self.company_id}, \
            name={self.name}, \
            bucket_url={self.bucket_url}, \
            id={self.id}, \
            created={self.created}\
        )"
    

    def set(self, bucket_url: str | None = None):
        if bucket_url:
            self.bucket_url = bucket_url
        return self


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Report.__annotations__):
            raise DictIncomplete(source)
        return Report(
            id = source["id"],
            company_id = source["company_id"],
            name = source["name"],
            bucket_url = source["bucket_url"],
            created = source["created"],
        )
    