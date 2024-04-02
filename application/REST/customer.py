from flask import Blueprint, jsonify, request
from application.REST import admin_token_required
from domain.entites.customer import Customer
from domain.services.customer_service import CustomerService


customers_blueprint = Blueprint('customers', __name__)
customer_service = CustomerService()


@customers_blueprint.route('/customers', methods=['GET'])
@admin_token_required
def get_customers():
    cursor, customers = customer_service.page()
    return jsonify({
        "cursor": cursor,
        "customers": [customer.to_dict() for customer in customers]
    })


@customers_blueprint.route('/customers/<customer_id>', methods=['GET'])
@admin_token_required
def get_customer(customer_id):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict())


@customers_blueprint.route('/customers', methods=['POST'])
@admin_token_required
def create_customer():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid json'}), 404  
    
    if not data.get('companyId'):
        return jsonify({'error': 'companyId not found!'}), 404
    company_id = data.get("companyId")
    
    if not data.get('name'):
        return jsonify({'error': 'name not found!'}), 404
    name = data.get("name")

    if not data.get('email'):
        return jsonify({'error': 'email not found!'}), 404
    email = data.get('email')

    if not data.get('password'):
        return jsonify({'error': 'password not found!'}), 404
    password = data.get('password')

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
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid json'}), 404  

    if not data.get('email'):
        return jsonify({'error': 'email not found!'}), 404
    email = data.get('email')

    if not data.get('password'):
        return jsonify({'error': 'password not found!'}), 404
    password = data.get('password')

    token = customer_service.get_token_by_email_and_password(email=email, password=password)
    return jsonify({
        "token": token
    }), 201
