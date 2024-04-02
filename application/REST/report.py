from flask import Blueprint, jsonify, request
from application.REST import admin_token_required, customer_token_required
from domain.entites.report import Report
from domain.services.report_service import ReportService


reports_blueprint = Blueprint('reports', __name__)
report_service = ReportService()


@reports_blueprint.route('/reports', methods=['GET'])
@customer_token_required
def get_reports():
    cursor, reports = report_service.page()
    return jsonify({
        "cursor": cursor,
        "reports": [report.to_dict() for report in reports]
    })


@reports_blueprint.route('/reports/<report_id>', methods=['GET'])
@customer_token_required
def get_report(report_id):
    report = report_service.get_by_id(report_id)
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    return jsonify(report.to_dict())


@reports_blueprint.route('/reports', methods=['POST'])
@admin_token_required
def create_report():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid json'}), 404  
    
    if not data.get('name'):
        return jsonify({'error': 'name not found!'}), 404
    name = data.get("name")

    if not data.get('companyId'):
        return jsonify({'error': 'companyId not found!'}), 404
    company_id = data.get('companyId')

    #TODO upload de arquivo
    report = report_service.create(
        Report(
            name=name,
            company_id=company_id,
        ),
        local_path=""
    )
    return jsonify(report.to_dict()), 201
