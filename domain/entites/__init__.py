import os
import hashlib
from datetime import datetime


class Entity:

    id: str | None
    created: datetime
    

    def to_dict(self):
        return vars(self)
    

class UserEntity(Entity):

    hashed_password: str | None

    
    def is_password_valid(self, password: str):
        if self.hash_password(password) ==  self.hashed_password:
            self.verified = True
            return True
        return False
    
    
    @staticmethod
    def hash_password(password: str) -> str:
        salted_password = f"{password}:{os.environ['PASSWORD_JWT_SECRET']}".encode('utf-8')
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(salted_password)        
        return hash_algorithm.hexdigest()
