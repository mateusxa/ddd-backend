import os
import jwt
from functools import wraps
from flask import request, jsonify
from domain.services.admin_service import AdminService
from domain.services.customer_service import CustomerService
# from utils.error import Error
# from main import app

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Authorization')
        if not token:
            return jsonify({'error': 'Missing token'}), 401

        try:
            kwargs['admin_id_token'] = AdminService.get_id_by_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated


def customer_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Missing token'}), 401

        try:
            kwargs['customer_id'], kwargs['company_id'] = CustomerService.get_id_and_company_id_by_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated
