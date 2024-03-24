from datetime import datetime


class ReportId:

    id: str

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id


class Report:

    company_id: str
    name: str
    data: str | bytes | None
    bucket_url: str | None
    id: ReportId | None
    created: datetime | None


    def __init__(
            self, company_id: str, name: str, data: str | bytes | None = None, bucket_url: str | None = None, 
            id: ReportId | None = None, created: datetime | None = None
        ):
        self.company_id = company_id
        self.name = name
        self.data = data
        self.bucket_url = bucket_url
        self.id = id
        self.created = created or datetime.now()


    def __repr__(self):
        return f"Report(\
            company_id={self.company_id}, \
            name={self.name}, \
            data={self.data}, \
            bucket_url={self.bucket_url}, \
            id={self.id}, \
            created={self.created}\
        )"
    

    def to_dict(self):
        return vars(self)


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in ["id", "company_id", "name", "bucket_url", "created"]):
            raise Exception(f"dict incomplete! {source}")
        return Report(
            id = ReportId(source["id"]),
            company_id = source["company_id"],
            name = source["name"],
            bucket_url = source["bucket_url"],
            created = source["created"],
        )
    