import jwt
from os import environ
from datetime import datetime, timezone
from utils.error import Error
from domain.entites.customer import Customer
from domain.repositories.customer_repository import CustomerRepository


class CustomerService:

    repository: CustomerRepository


    def __init__(self, ):
        self.repository = CustomerRepository()


    def create(self, customer: Customer) -> Customer:
        if self.get_by_email(customer.email):
            raise Error(Error.Code.invalid_attribute, f"Customer email already exists!", 400)
        return self.repository.create(customer)
    

    def create_with_token(self, token: str, name: str, email: str, password: str) -> Customer:
        decoded_payload = jwt.decode(token, environ["INVITE_JWT_SECRET"], algorithms=['HS256'])

        if datetime.now(timezone.utc).timestamp() > float(decoded_payload["expires_after"]):
            Error(Error.Code.token_expired, f"Token expiration: {decoded_payload['expires_after']}", 400)
        
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
        if not customer:
            raise Error(Error.Code.object_not_found, f"No customer with id: {customer_id}!", 400)
        if password:
            customer.hashed_password = password
        return self.repository.update(customer)


    def page(self, cursor: str | None = None, limit: int | None = None):
        return self.repository.page(cursor=cursor, limit=limit)


    def get_by_id(self, customer_id: str) -> Customer | None:
        return self.repository.get_by_id(customer_id)
    

    def get_by_email(self, email: str) -> Customer | None:
        customer_list = self.repository.get_by_fields(email=email)
        if len(customer_list) > 1:
            raise Error(Error.Code.internal_error, f"More than 1 Customer with same email: {email}", 500)
        return customer_list[0] if len(customer_list) > 0 else None


    def get_token_by_email_and_password(self, email: str, password: str) -> str:
        customer = self.get_by_email(email)
        if not customer or not customer.id:
            raise Error(Error.Code.invalid_attribute, f"Invalid email!", 400)
        if not customer.is_password_valid(password):
            raise Error(Error.Code.invalid_attribute, f"Invalid password!", 400)
        token = jwt.encode({
            "id": customer.id,
            "companyId": customer.company_id,
        }, environ['CUSTOMER_JWT_SECRET'])
        return token


    @staticmethod
    def get_id_and_company_id_by_token(token: str) -> tuple[str, str]:
        payload = jwt.decode(token, environ['CUSTOMER_JWT_SECRET'], verify=True, algorithms=["HS256"])
        return payload["id"], payload["companyId"]
