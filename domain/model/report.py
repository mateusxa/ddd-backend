
import datetime


class Report:

    def __init__(self, id: str, company_id: str, name: str, bucket_url: str = None):
        self.id = id
        self.company_id = company_id
        self.name = name
        self.bucket_url = bucket_url
        self.created = datetime.utcnow()