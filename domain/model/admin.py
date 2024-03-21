
import datetime


class Admin:

    def __init__(self, id: str, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = self._hashPassword(password)
        self.created = datetime.utcnow()

    def _hashPassword(password: str) -> str:
        raise NotImplemented