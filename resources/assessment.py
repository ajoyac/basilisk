from flask import request
from flask_restful import Resource

from Model import db, Assessment,AssessmentSchema
import flask_jwt_extended

assessment_schema = AssessmentSchema()

class Assessments(Resource):
    @flask_jwt_extended.jwt_required
    def get(self,question_id):
        assessments = Assessment.query.filter_by(question_id=int(question_id)).all()
        if assessments:
            result = []
            for assessment in assessments:
                result.append(assessment_schema.dump(assessment).data)
            return result,201
        else:
            return {'message': 'No paramater found.'}, 404

    @flask_jwt_extended.jwt_required
    def post(self,question_id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = assessment_schema.load(json_data)
        if errors:
            return errors, 400
        print(data)
        assessment = Assessment(
            question_id =  data["question_id"],
            parameters = data['parameters'],
            answer = data["answer"]
            )
        assessment.save()
        result = assessment_schema.dump(assessment).data
  
        return { "status": 'success', 'data': result }, 201