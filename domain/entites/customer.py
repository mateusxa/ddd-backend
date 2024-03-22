import hashlib
from datetime import datetime
from utils.constants import SALT


class Customer:

    company_id: str
    name: str
    email: str
    hased_password: str | None
    id: str | None
    created: datetime | None


    def __init__(self, company_id: str, name: str, email: str, password: str | None = None, hased_password: str | None = None, id: str | None = None, created: datetime | None = None):
        self.company_id = company_id
        self.name = name
        self.email = email
        self.hased_password = self.__hash_password(password) if password else hased_password
        self.created = created or datetime.now()


    def verify_password(self, password: str):
        if self.__hash_password(password) ==  self.hased_password:
            self.verified = True
            return True
        return False


    @staticmethod
    def from_dict(dict: dict):
        if not all(attr in dict for attr in Customer.__annotations__):
            raise Exception(f"dict incomplete! {dict}")
        return Customer(
            id = dict["id"],
            company_id = dict["company_id"],
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
    