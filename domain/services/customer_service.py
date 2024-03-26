from datetime import datetime
from repository.reposity import Repository
from domain.entites.report import Report
from domain.entites.customer import Customer, CustomerId


class CustomerService:

    repository: Repository


    def __init__(self, ):
        self.repository = Repository()


    def create(self, customer: Customer) -> Customer:
        # TODO send email to customers email customer will then update itself
        customer_dict = self.repository.save(customer)
        return Customer.from_dict(customer_dict)
    

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
