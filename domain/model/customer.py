
import datetime


class Customer:

    def __init__(self, id: str, company_id: str, name: str, email: str, password: str):
        self.id = id
        self.company_id = company_id
        self.name = name
        self.email = email
        self.password = self._hashPassword(password)
        self.created = datetime.utcnow()

    def _hashPassword(password: str) -> str:
        raise NotImplemented