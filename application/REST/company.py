from flask import Blueprint, jsonify, request
from domain.entites.company import Company
from domain.services.company_service import CompanyService
from utils.error import Error


companies_blueprint = Blueprint('companies', __name__)
company_service = CompanyService()


@companies_blueprint.route('/companies', methods=['GET'])
def get_companies():
    cursor = request.args.get('cursor')
    limit = request.args.get('limit')
    
    limit = int(limit) if limit else None
    cursor, companies = company_service.page(cursor=cursor, limit=limit)
    return jsonify({
        "cursor": cursor,
        "companies": [company.to_dict() for company in companies]
    })


@companies_blueprint.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    company = company_service.get_by_id(company_id)
    if not company:
        raise Error(Error.Code.object_not_found, f"No company with id: {company_id}!", 400)
    return jsonify(company.to_dict())


@companies_blueprint.route('/companies', methods=['POST'])
def create_company():
    data: dict | None = request.json

    required_attributes = ["name", "tax_id"]
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

    name = data["name"]
    tax_id = data["tax_id"]

    company = company_service.create(
        Company(
            name=name,
            tax_id=tax_id,
        )
    )
    return jsonify(company.to_dict()), 201
