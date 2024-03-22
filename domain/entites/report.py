from datetime import datetime


class Report:

    company_id: str
    name: str
    data: str | bytes | None
    bucket_url: str | None
    id: str | None
    created: datetime | None


    def __init__(self, company_id: str, name: str, data: str | bytes | None = None, bucket_url: str | None = None, id: str | None = None, created: datetime | None = None):
        self.company_id = company_id
        self.name = name
        self.data = data
        self.bucket_url = bucket_url
        self.id = id
        self.created = created or datetime.now()


    @staticmethod
    def from_dict(dict: dict):
        if not all(attr in dict for attr in ["id", "company_id", "name", "bucket_url", "created"]):
            raise Exception(f"dict incomplete! {dict}")
        return Report(
            id = dict["id"],
            company_id = dict["company_id"],
            name = dict["name"],
            bucket_url = dict["bucket_url"],
            created = dict["created"],
        )
    