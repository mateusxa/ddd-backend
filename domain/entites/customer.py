import os
import hashlib
from datetime import datetime, timezone
from utils.error import Error
from domain.entites import Entity



class Customer(Entity):

    def __init__(
        self, company_id: str, name: str, email: str, password: str, 
        id: str | None = None, created: datetime | None = None
    ):
        self._company_id = company_id
        self._name = name
        self._email = email
        self._id = id
        self._password = password
        self._created = created or datetime.now(timezone.utc)

    @property
    def company_id(self) -> str:
        return  self._company_id

    @property
    def name(self) -> str:
        return  self._name
    
    @property
    def email(self) -> str:
        return  self._email
    
    @property
    def password(self) -> str:
        return  self._password
    
    @password.setter
    def password(self, password: str):
        self._password = password
    
    @property
    def id(self) -> str | None:
        return  self._id
    
    @property
    def created(self) -> datetime:
        return  self._created

    def __repr__(self):
        return f"Customer(\
            company_id={self.company_id}, \
            name={self.name}, \
            email={self.email}, \
            password={self.password}, \
            id={self.id}, \
            created={self.created}\
        )"

    def is_password_valid(self, password: str):
        if self.hash_password(password) ==  self.password:
            self.verified = True
            return True
        return False

    @staticmethod
    def hash_password(password: str) -> str:
        salted_password = f"{password}:{os.environ['PASSWORD_JWT_SECRET']}".encode('utf-8')
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(salted_password)        
        return hash_algorithm.hexdigest()
    

    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Customer.__annotations__):
            raise Error(Error.Code.internal_error, str(source), 500)
        return Customer(
            id = source["id"],
            company_id = source["company_id"],
            name = source["name"],
            email = source["email"],
            password = source["password"],
            created = source["created"],
        )
