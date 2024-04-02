from flask import Blueprint, jsonify, request
from domain.entites.company import Company
from domain.services.company_service import CompanyService


companies_blueprint = Blueprint('companies', __name__)
company_service = CompanyService()


@companies_blueprint.route('/companies', methods=['GET'])
def get_companies():
    cursor, companies = company_service.page()
    return jsonify({
        "cursor": cursor,
        "companies": [company.to_dict() for company in companies]
    })


@companies_blueprint.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    company = company_service.get_by_id(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    return jsonify(company.to_dict())


@companies_blueprint.route('/companies', methods=['POST'])
def create_company():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid json'}), 404  
    
    if not data.get('name'):
        return jsonify({'error': 'name not found!'}), 404
    name = data.get("name")

    if not data.get('taxId'):
        return jsonify({'error': 'taxId not found!'}), 404
    tax_id = data.get('taxId')

    company = company_service.create(
        Company(
            name=name,
            tax_id=tax_id,
        )
    )
    return jsonify(company.to_dict()), 201
