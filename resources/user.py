from flask import request
from flask_restful import Resource
from Model import db, User,UserSchema

user_schema = UserSchema()

class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'message': 'user already exists'}, 400
        user = User(
            username=json_data['username'],
            password = json_data['password']
            )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return { "status": 'success', 'data': result }, 201