from flask_restful import Resource, request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token

from user import User

users = [
    User(1, 'anon', '123')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = username_mapping.get(data['username'], None)
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                'message': 'Successfully logged in',
                'access_token': access_token,
            }, 200

        return {'message': 'Failed to log in'}, 401
