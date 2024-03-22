from repository.reposity import Repository
from domain.entites.report import Report
from domain.entites.customer import Customer


class CustomerService:

    customer: Customer

    def __init__(self, customer: Customer):
        self.customer = customer


    def get_reports(self):
        matching_dicts = []
        for d in Repository.get_all():
            if d.get("company_id") == self.customer.company_id:
                matching_dicts.append(Report.from_dict(d))
        return matching_dicts
