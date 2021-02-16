from flask_restful import Resource, request, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token

from user import User
from request_parser import AuthParser

# We can add json parser for validating the data
# We can check if user exists before registering


class UserLogin(Resource):
    def post(self):
        data = AuthParser.parser.parse_args(req=request)
        user = User.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                'message': 'Successfully logged in',
                'access_token': access_token,
            }, 200

        return {'message': 'Failed to log in'}, 401


class UserRegister(Resource):
    def post(self):
        data = AuthParser.parser.parse_args(req=request)

        if User.find_by_username(data['username']):
            return {'message': 'This user already exists'}, 400

        user = User.add_user(User(None, data['username'], data['password']))

        # Bad code below, dont return password
        return {'message': 'Successfully created account',
                'username': user.username,
                'password': user.password,
                }, 201
