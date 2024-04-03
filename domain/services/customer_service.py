import jwt
from os import environ
from datetime import datetime, timezone
from domain.entites.customer import Customer
from domain.repositories.customer_repository import CustomerRepository
from utils.error import DuplicatedAttribute, DuplicatedEntities, InvalidAttribute, ObjectNotFound, TokenExpired


class CustomerService:

    repository: CustomerRepository


    def __init__(self, ):
        self.repository = CustomerRepository()


    def create(self, customer: Customer) -> Customer:
        if self.get_by_email(customer.email):
            raise DuplicatedAttribute(f"Customer name {customer.name} already exists!")
        customer_dict = self.repository.add(customer.to_dict())
        return Customer.from_dict(customer_dict)
    

    def create_with_token(self, token: str, name: str, email: str, password: str):
        decoded_payload = jwt.decode(token, environ["INVITE_JWT_SECRET"], algorithms=['HS256'])

        if datetime.now(timezone.utc).timestamp() > float(decoded_payload["expires_after"]):
            raise TokenExpired(f"Token expiration: {decoded_payload['expires_after']}")
        
        return self.create(
            Customer(
                company_id=decoded_payload["company_id"],
                name=name,
                email=email,
                password=password,
            )
        )
    

    def delete(self, customer_id: str) -> None:
        return self.repository.delete(customer_id)


    def update(self, customer_id: str, password: str | None = None) -> Customer:
        customer = self.get_by_id(customer_id)
        return customer.set(password)


    def get_by_id(self, customer_id: str):
        customer_dict = self.repository.get_by_id(customer_id)
        if customer_dict:
            return Customer.from_dict(customer_dict)
        raise ObjectNotFound(f"No customers with {customer_id}")
    

    def get_by_email(self, email: str) -> Customer | None:
        customer_list = [Customer.from_dict(customer_dict) for customer_dict in self.repository.get_by_fields(email=email)]
        if len(customer_list) > 1:
            raise DuplicatedEntities(f"More than 1 Customer with same email: {email}")
        
        return customer_list[0] if len(customer_list) > 0 else None


    def get_token_by_email_and_password(self, email: str, password: str) -> str:
        customer = self.get_by_email(email)
        if not customer or not customer.id:
            raise InvalidAttribute("Invalid email!")
        if not customer.is_password_valid(password):
            raise InvalidAttribute("Invalid password!")
        token = jwt.encode({
            "id": customer.id,
            "companyId": customer.company_id,
        }, environ['CUSTOMER_JWT_SECRET'])
        return token


    @staticmethod
    def get_id_and_company_id_by_token(token: str) -> tuple[str, str]:
        payload = jwt.decode(token, environ['CUSTOMER_JWT_SECRET'], verify=True, algorithms=["HS256"])
        return payload["id"], payload["companyId"]
    

    def page(self, cursor: str | None = None, limit: int | None = None):
        new_cursor, customers_dict = self.repository.page(cursor=cursor, limit=limit)
        return new_cursor, [Customer.from_dict(customer) for customer in customers_dict if customer]
