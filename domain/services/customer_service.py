from repository.reposity import Repository
from domain.entites.report import Report
from domain.entites.customer import Customer


class CustomerService:

    repository: Repository

    def __init__(self, ):
        self.repository = Repository()


    def create(self, customer: Customer) -> Customer:
        # TODO send email to customers email customer will then update itself
        customer_dict = self.repository.save(customer)
        return Customer.from_dict(customer_dict)
    

    def get_all(self):
        pass
        # TODO rework
        # matching_dicts = []
        # for d in self.repository.get_all(Report(company_id = "", name = "")):
        #     if d.get("company_id") == self.customer.company_id:
        #         matching_dicts.append(Report.from_dict(d))
        # return matching_dicts
