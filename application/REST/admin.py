from logging import warning
from flask import Blueprint, jsonify, request
from application.REST import admin_token_required
from domain.entites.admin import Admin
from domain.services.admin_service import AdminService


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
        return jsonify({'error': 'Admin not found'}), 404
    return jsonify(admin.to_dict())


@admins_blueprint.route('/admins', methods=['POST'])
@admin_token_required
def create_admin(admin_id_token):
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid json'}), 404  
    
    if not data.get('name'):
        return jsonify({'error': 'name not found!'}), 404
    name = data.get("name")

    if not data.get('email'):
        return jsonify({'error': 'email not found!'}), 404
    email = data.get('email')

    if not data.get('password'):
        return jsonify({'error': 'password not found!'}), 404
    password = data.get('password')

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
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid json'}), 404  

    if not data.get('email'):
        return jsonify({'error': 'email not found!'}), 404
    email = data.get('email')

    if not data.get('password'):
        return jsonify({'error': 'password not found!'}), 404
    password = data.get('password')

    token = admin_service.get_token_by_email_and_password(email=email, password=password)
    return jsonify({
        "token": token
    }), 201
