
from flask import Blueprint
from flask_restful import Api
from resources.user import Register,Login
from resources.question import Questions, AQuestion
from resources.assessment import Assessments
from resources.completed import Complete


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Register, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Questions,'/question')
api.add_resource(AQuestion,'/question/<int:id>')
api.add_resource(Assessments,'/question/<int:question_id>/parameter')
api.add_resource(Complete, '/completed')
