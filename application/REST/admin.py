from logging import error
from flask import Blueprint, jsonify, request
from application.REST import admin_token_required
from domain.entites.admin import Admin
from domain.services.admin_service import AdminService
from utils.error import Error


admins_blueprint = Blueprint('admins', __name__)
admin_service = AdminService()


@admins_blueprint.route('/admins', methods=['GET'])
@admin_token_required
def get_admins(admin_id_token):
    cursor = request.args.get('cursor')
    limit = request.args.get('limit')

    limit = int(limit) if limit else None
    new_cursor, admins = admin_service.page(cursor=cursor, limit=limit)
    return jsonify({
        "cursor": new_cursor,
        "admins": [admin.to_dict() for admin in admins]
    })


@admins_blueprint.route('/admins/<admin_id>', methods=['GET'])
@admin_token_required
def get_admin(admin_id_token, admin_id):
    admin = admin_service.get_by_id(admin_id)
    if not admin:
        raise Error(Error.Code.object_not_found, f"No admin with id: {admin_id}!", 400)
    return jsonify(admin.to_dict())


@admins_blueprint.route('/admins', methods=['POST'])
@admin_token_required
def create_admin(admin_id_token):
    # TODO jogar no middleware
    data: dict | None = request.json

    required_attributes = ["name", "email", "password"]
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
    email = data["email"]
    password = data["password"]

    admin = admin_service.create(
        Admin(
            name=name,
            email=email,
            password=password,
        )
    )

    return jsonify(admin.to_dict()), 201


@admins_blueprint.route('/admins/token', methods=['POST'])
def create_admin_token():
    data: dict | None = request.json

    required_attributes = ["name", "password"]
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
    
    email = data["email"]
    password = data["password"]

    token = admin_service.get_token_by_email_and_password(email=email, password=password)

    return jsonify({
        "token": token
    }), 201
