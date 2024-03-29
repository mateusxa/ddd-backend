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
    

    def get_by_email(self, email: str):
        customer_list = [Customer.from_dict(customer_dict) for customer_dict in self.repository.get_by_fields("customers", email=email)]
        return customer_list[0]

    def get_token_by_email_and_password(self, email: str, password: str) -> str:
        customer = self.get_by_email(email)
        if not customer or not customer.id:
            raise Exception("Invalid email!")
        if not customer.is_password_valid(password):
            raise Exception("Invalid password!")
        token = jwt.encode({
            "id": customer.id.value,
            "companyId": customer.company_id,
        }, os.environ['CUSTOMER_JWT_SECRET'])
        return token

    @staticmethod
    def get_id_and_company_id_by_token(token: str) -> tuple[str, str]:
        payload = jwt.decode(token, os.environ['CUSTOMER_JWT_SECRET'], verify=True, algorithms=["HS256"])
        return payload["id"], payload["companyId"]

    def update(self, customer_id: CustomerId, password: str | None = None) -> Customer:
        customer = self.get_by_id(customer_id)
        return customer.set(password)
    

    def page(self, cursor: str | None = None, limit: int | None = None):
        new_cursor, customers_dict = self.repository.page("customers", cursor=cursor, limit=limit)
        return new_cursor, [Customer.from_dict(customer) for customer in customers_dict if customer]
