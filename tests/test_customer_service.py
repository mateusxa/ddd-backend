import uuid
from domain.entites.customer import Customer
from domain.services.customer_service import CustomerService


def test_create_customer():
    name = "name"
    email = "email"
    password = "password"
    company_id = str(uuid.uuid4())
    
    customer_service = CustomerService()

    customer = customer_service.create(
        Customer(
            company_id = company_id,
            name = name,
            email = email,
            password = password,
        )
    )

    assert customer.name == name
    assert customer.email == email
    assert customer.hashed_password != password


# def test_get_reports():
#     name = "TestCompany"

#     ADMIN.verify_password(ADMIN_PASSWORD)
#     admin_service = AdminService(ADMIN)

#     report = admin_service.create_report(
#         Report(
#             company_id = company_id,
#             name = name,
#         ),
#         local_path = "/home/mateus/projects/xpaEnghenharia/tests/image.jpeg",
#     )

#     customer_service = CustomerService(customer)
#     for report in customer_service.get_reports():
#         assert report.id != None
#         assert report.company_id == company_id


