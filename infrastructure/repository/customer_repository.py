from domain.entites.customer import Customer
from infrastructure.data_mapper.sqlalchemy.customer import customer_entity_to_model, customer_model_to_entity
from infrastructure.models.sqlalchemy.customer import CustomerModel
from infrastructure.repository import Repository
from utils.error import Error


class CustomerRepository(Repository):

    entity_name: str

    def __init__(self):
        super().__init__()
        self.entity_name = "customers"


    def create(self, customer: Customer) -> Customer:
        instance = customer_entity_to_model(customer)
        self.session.add(instance)
        self.session.commit()
        return customer_model_to_entity(instance)
        

    def get_by_id(self, customer_id: str) -> Customer | None:
        instance = self.session.get(CustomerModel, customer_id)
        if not instance:
            return None
        return customer_model_to_entity(instance)


    def get_by_email(self, email) -> Customer | None:
        instance = self.session.query(CustomerModel).filter_by(email=email).first()
        if not instance:
            return None
        return customer_model_to_entity(instance)

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Customer]]:
        customer_id = self.decode_cursor(cursor)
        instances = self.session.query(CustomerModel).filter_by(id=customer_id).limit(limit).all()
        
        new_cursor = None
        customer_list = []
        for instance in instances:
            customer = customer_model_to_entity(instance)
            customer_list.append(customer)
            if not customer.id:
                raise Error(Error.Code.internal_error, "Mapped customer without id", 500)
            new_cursor = customer.id

        new_cursor = self.encode_cursor(new_cursor)
        return new_cursor,  customer_list


    def update(self, customer: Customer) -> Customer:
        if not customer.id:
            # TODO fix error  
            raise Error("update", "update")
        
        instance = self.session.get(CustomerModel, customer.id)
        if not instance:
            # TODO fix error
            raise Error("not exists", "object not exists")
        
        instance.name = customer.name
        instance.password = customer.password
        self.session.commit()
        return customer_model_to_entity(instance)


    def delete(self, customer_id: str) -> None:
        customer_model = self.session.get(CustomerModel, customer_id)
        self.session.delete(customer_model)   
        self.session.commit()

    
    def __getitem__(self, key):
        return self.get_by_id(key)
    