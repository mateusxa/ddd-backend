from flask import Blueprint, jsonify, request
from application.REST import admin_token_required, customer_token_required
from domain.entites.report import Report
from domain.services.report_service import ReportService
from utils.error import Error


reports_blueprint = Blueprint('reports', __name__)
report_service = ReportService()


@reports_blueprint.route('/reports', methods=['GET'])
@customer_token_required
def get_reports(customer_id, company_id):
    cursor = request.args.get('cursor')
    limit = request.args.get('limit')

    limit = int(limit) if limit else None
    new_cursor, reports = report_service.page(cursor=cursor, limit=limit)
    return jsonify({
        "cursor": new_cursor,
        "reports": [report.to_dict() for report in reports]
    })


@reports_blueprint.route('/reports/<report_id>', methods=['GET'])
@customer_token_required
def get_report(report_id):
    report = report_service.get_by_id(report_id)
    if not report:
        raise Error(Error.Code.object_not_found, f"No report with id: {report_id}!", 400)
    return jsonify(report.to_dict())


@reports_blueprint.route('/reports', methods=['POST'])
@admin_token_required
def create_report():
    # TODO jogar no middleware
    data: dict | None = request.json

    required_attributes = ["name", "company_id", "password"]
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
    company_id = data["company_id"]

    #TODO upload de arquivo
    report = report_service.create(
        Report(
            name=name,
            company_id=company_id,
        ),
        local_path=""
    )
    return jsonify(report.to_dict()), 201
