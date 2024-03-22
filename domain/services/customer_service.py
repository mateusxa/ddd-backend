import uuid
from domain.entites.customer import Customer
from domain.entites.company import Company
from domain.entites.customer import Customer
from domain.entites.report import Report
from repository.reposity import Repository


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
