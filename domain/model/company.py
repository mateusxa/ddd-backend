
import datetime


class Company:

    def __init__(self, id: str, company_id: str, name: str, taxId: str):
        self.id = id
        self.company_id = company_id
        self.name = name
        self.taxId = taxId
        self.created = datetime.utcnow()