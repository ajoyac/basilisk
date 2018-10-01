from flask import request
from flask_restful import Resource

from Model import db,Assessment, Completed,CompletedSchema
import flask_jwt_extended

completed_schema = CompletedSchema()

class Complete(Resource):
    @flask_jwt_extended.jwt_required
    def get(self):
        user_id = flask_jwt_extended.get_jwt_identity()["id"]
        completed = Completed.query.filter_by(user_id=int(user_id)).all()
        if completed:
            result = []
            for complete in completed:
                result.append(completed_schema.dump(complete).data)
            return result,201
        else:
            return {'message': 'No paramater found.'}, 404

    @flask_jwt_extended.jwt_required
    def post(self):
        json_data = request.get_json(force=True)
        json_data["user_id"] = flask_jwt_extended.get_jwt_identity()["id"]
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = completed_schema.load(json_data)
        if errors:
            return errors, 400
        print(data)
        assessment = Assessment.query.get(json_data['question_id'])
        if assessment:
            if assessment.answer == json_data["answer"]:
                already_completed = Completed.query.filter_by(
                    question_id=data['question_id'],user_id = data['user_id']).first()
                if already_completed:
                    return {"message": 'Correct Answer!'}
                completed = Completed(
                    question_id =  data["question_id"],
                    user_id = data['user_id'],
                )
                completed.save()
                result = completed_schema.dump(completed).data

                return { "status": 'success', 
                    "message": 'Correct Answer!', 'data': result }, 201

        return {"message":"Wrong Answer"}
        
