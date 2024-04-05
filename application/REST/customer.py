from flask import Blueprint, jsonify, request
from application.REST import admin_token_required
from domain.entites.customer import Customer
from domain.services.customer_service import CustomerService
from utils.error import Error


customers_blueprint = Blueprint('customers', __name__)
customer_service = CustomerService()


@customers_blueprint.route('/customers', methods=['GET'])
@admin_token_required
def get_customers():
    cursor = request.args.get('cursor')
    limit = request.args.get('limit')

    limit = int(limit) if limit else None
    new_cursor, customers = customer_service.page(cursor=cursor, limit=limit)
    return jsonify({
        "cursor": new_cursor,
        "customers": [customer.to_dict() for customer in customers]
    })


@customers_blueprint.route('/customers/<customer_id>', methods=['GET'])
@admin_token_required
def get_customer(customer_id):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise Error(Error.Code.object_not_found, f"No customer with id: {customer_id}!", 400)
    return jsonify(customer.to_dict())


@customers_blueprint.route('/customers', methods=['POST'])
@admin_token_required
def create_customer():
    data: dict | None = request.json

    required_attributes = ["company_id", "name", "email", "password"]
    if not data:
        raise Error(
            code = Error.Code.missing_attributes, 
            message = Error.Message.missing_attributes.format(attributes=required_attributes),
            status_code = 400
        )
    
    attributes_in_json = [field for field in data.keys()] 
    missing_attributes_in_json = [item for item in required_attributes if item not in attributes_in_json]    

    if len(missing_attributes_in_json) < 0:
        raise Error(
            code = Error.Code.missing_attributes, 
            message = Error.Message.missing_attributes.format(attributes=missing_attributes_in_json),
            status_code = 400
        )
    ### 
    company_id = data["company_id"]
    name = data["name"]
    email = data["email"]
    password = data["password"]

    customer = customer_service.create(
        Customer(
            company_id=company_id,
            name=name,
            email=email,
            password=password,
        )
    )
    return jsonify(customer.to_dict()), 201


@customers_blueprint.route('/customers/token', methods=['POST'])
def create_customer_token():
    # TODO jogar no middleware
    data: dict | None = request.json

    required_attributes = ["email", "password"]
    if not data:
        raise Error(
            code = Error.Code.missing_attributes, 
            message = Error.Message.missing_attributes.format(attributes=required_attributes),
            status_code = 400
        )
    
    attributes_in_json = [field for field in data.keys()] 
    missing_attributes_in_json = [item for item in required_attributes if item not in attributes_in_json]    

    if len(missing_attributes_in_json) < 0:
        raise Error(
            code = Error.Code.missing_attributes, 
            message = Error.Message.missing_attributes.format(attributes=missing_attributes_in_json),
            status_code = 400
        )
    ### 

    email = data["email"]
    password = data["password"]

    token = customer_service.get_token_by_email_and_password(email=email, password=password)
    return jsonify({
        "token": token
    }), 201
