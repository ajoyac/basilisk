from flask import request
from flask_restful import Resource
import flask_jwt_extended
from Model import db, User,UserSchema

user_schema = UserSchema()


class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 400
        user = User.query.filter_by(username=data['username'],password=data['password']).first()
        if user:
            result = user_schema.dump(user).data
            del result["password"]
            token = flask_jwt_extended.create_access_token(identity=result)
            result ["token"] = token
            return { "status": 'success', 'data': result }, 201
        else:
             return {'message': 'No user/password found'}, 400   




class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 400
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'message': 'user already exists'}, 400
        user = User(
            username=json_data['username'],
            password = json_data['password']
            )
        user.save()

        result = user_schema.dump(user).data
        del result["password"]
        
        token = flask_jwt_extended.create_access_token(identity=result)
        result ["token"] = token
      

        return { "status": 'success', 'data': result }, 201