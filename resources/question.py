from flask import request
from flask_restful import Resource

from Model import db, Question,QuestionSchema
import flask_jwt_extended

question_schema = QuestionSchema()

class AQuestion(Resource):
    @flask_jwt_extended.jwt_required
    def get(self,id):
        question = Question.query.get(id)
        if question:
            result = question_schema.dump(question).data
            return result,201
        else:
            return {'message': 'No quesion found.'}, 404
class Questions(Resource):
    @flask_jwt_extended.jwt_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = question_schema.load(json_data)
        if errors:
            return errors, 400
        question = Question.query.filter_by(question=data['question']).first()
        if question:
            return {'message': 'user already exists'}, 400
        question = Question(
            question=json_data['question']
            )
        question.save()


        result = question_schema.dump(question).data
  
        return { "status": 'success', 'data': result }, 201