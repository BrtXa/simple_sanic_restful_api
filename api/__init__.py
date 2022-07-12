from sanic import Blueprint
from sanic_openapi import openapi2_blueprint
from api.transaction_blueprint import transaction_bp

api = Blueprint.group([openapi2_blueprint, transaction_bp], url_prefix="")
