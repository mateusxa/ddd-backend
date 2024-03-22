import hashlib
from logging import warn
from datetime import datetime

from utils.constants import SALT

class Admin:
    name: str
    email: str
    hased_password: str | None
    id: str | None
    created: datetime | None

    def __init__(self, name: str, email: str, password: str | None = None, hased_password: str | None = None, id: str | None = None, created: datetime | None = None):
        self.name = name
        self.email = email
        self.hased_password = self.__hash_password(password) if password else hased_password
        self.id = id
        self.created = created or datetime.now()

    def verify_password(self, password: str):
        if self.__hash_password(password) ==  self.hased_password:
            self.verified = True
            return True
        return False
    
    @staticmethod
    def from_dict(dict: dict):
        if not all(attr in dict for attr in Admin.__annotations__):
            raise Exception(f"dict incomplete! {dict}")
        return Admin(
            id = dict["id"],
            name = dict["name"],
            email = dict["email"],
            hased_password = dict["hased_password"],
            created = dict["created"],
        )
    
    @staticmethod
    def __hash_password(password: str) -> str:
        salted_password = f"{password}:{SALT}".encode('utf-8')
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(salted_password)        
        return hash_algorithm.hexdigest()
