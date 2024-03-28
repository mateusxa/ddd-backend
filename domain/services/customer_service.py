import os
import jwt
from datetime import datetime, timezone
from repository.reposity import Repository
from domain.entites.customer import Customer, CustomerId


class CustomerService:

    repository: Repository


    def __init__(self, ):
        self.repository = Repository()


    def create(self, customer: Customer) -> Customer:
        customer_dict = self.repository.save(customer)
        return Customer.from_dict(customer_dict)
    

    def create_with_token(self, token: str, name: str, email: str, password: str):
        decoded_payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=['HS256'])

        if datetime.now(timezone.utc).timestamp() > float(decoded_payload["expires_after"]):
            raise Exception("Token expired!")
        
        return self.create(
            Customer(
                company_id=decoded_payload["company_id"],
                name=name,
                email=email,
                password=password,
            )
        )
    

    def get_by_id(self, customer_id: CustomerId):
        customer_dict = self.repository.get_by_id(customer_id)
        if customer_dict:
            return Customer.from_dict(customer_dict)
        raise Exception(f"No customers with {customer_id}")
    

    def update(self, customer_id: CustomerId, password: str | None = None) -> Customer:
        customer = self.get_by_id(customer_id)
        return customer.set(password)
    

    def page(self, last_created: datetime | None = None, limit: int | None = None):
        return self.repository.page("customers", last_created=last_created, limit=limit)
