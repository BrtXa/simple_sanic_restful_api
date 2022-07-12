from sanic import Blueprint
# from sanic_openapi import openapi3_blueprint
from api.transaction_blueprint import transaction_bp

api = Blueprint.group([transaction_bp], url_prefix="")
