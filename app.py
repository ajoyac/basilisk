
from flask import Blueprint
from flask_restful import Api
from resources.user import Register,Login


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Register, '/signup')
api.add_resource(Login, '/login')