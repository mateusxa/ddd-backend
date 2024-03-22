from repository.reposity import Repository
from domain.entites.admin import Admin
from domain.entites.report import Report
from domain.entites.company import Company
from domain.entites.customer import Customer


# def validate_admin(func):
#     def wrapper(self, *args, **kwargs):
#         # TODO check via repository if 
#         print(self)
#         if not self.admin.verified:
#             raise PermissionError("Unauthorized: Admin validation failed.")
#         return func(self, *args, **kwargs)
#     return wrapper


class AdminService:

    admin: Admin


    def __init__(self, admin: Admin):
        self.admin = admin


    def create_admin(self):
        admin_dict = Repository.save(vars(self.admin))
        return Admin.from_dict(admin_dict)


    # @validate_admin
    def create_company(self, company: Company) -> Company:
        company_dict = Repository.save(vars(company))
        return Company.from_dict(company_dict)


    def get_company(self, company_id: str):
        company_dict = Repository.get_by_id(company_id)
        if company_dict:
            return Company.from_dict(company_dict)
        raise Exception(f"No companies with {company_id}")
    

    def create_report(self, report: Report) -> Report:
        old_report_dict = vars(report)
        del old_report_dict["data"]
        report_dict = Repository.save(vars(report))
        return Report.from_dict(report_dict)
    

    def delete_report(self, report_id: str) -> None:
        return Repository.delete(report_id)
    

    def get_report(self, report_id: str):
        report_dict = Repository.get_by_id(report_id)
        if report_dict:
            return Report.from_dict(report_dict)
        raise Exception(f"No reports with {report_id}")
    

    def create_customer(self, customer: Customer) -> Customer:
        # TODO send email to customers email customer will then update itself
        customer_dict = Repository.save(vars(customer))
        return Customer.from_dict(customer_dict)
