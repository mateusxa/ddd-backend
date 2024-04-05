from repository.reposity import Repository
from domain.entites.customer import Customer
from infrastructure.firebase.firestore import Firestore


class CustomerRepository(Repository):

    entity_name: str

    def __init__(self):
        self.entity_name = "customers"
        self.db = Firestore()


    def create(self, customer: Customer) -> Customer:
        return Customer.from_dict(self.db.create(self.entity_name, customer.to_dict()))
        

    def get_by_id(self, customer_id: str) -> Customer | None:
        customer_dict = self.db.get_by_id(self.entity_name, customer_id)
        return Customer.from_dict(customer_dict) if customer_dict else None


    def get_by_fields(self, limit: int | None = None, **kwargs) -> list[Customer]:
        return [Customer.from_dict(customer_dict) for customer_dict in self.db.get_by_fields(self.entity_name, limit=limit, **kwargs)]

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Customer]]:
        new_cursor, customer_list = self.db.page(self.entity_name, cursor=cursor, limit=limit, **kwargs)
        return new_cursor, [Customer.from_dict(customer_dict) for customer_dict in customer_list]


    def update(self, customer: Customer) -> Customer:
        return Customer.from_dict(self.db.update(self.entity_name, customer.to_dict()))


    def delete(self, customer_id: str) -> None:
        return self.db.delete(self.entity_name, customer_id)    
