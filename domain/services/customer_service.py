from repository.reposity import Repository
from domain.entites.report import Report
from domain.entites.customer import Customer


class CustomerService:

    customer: Customer
    repository: Repository

    def __init__(self, customer: Customer):
        self.customer = customer
        self.repository = Repository()


    def get_reports(self):
        # TODO rework
        matching_dicts = []
        for d in self.repository.get_all("reports"):
            if d.get("company_id") == self.customer.company_id:
                matching_dicts.append(Report.from_dict(d))
        return matching_dicts
