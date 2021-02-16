from flask import Flask
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from security import UserLogin, UserRegister
from items import Item, ItemList

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=4242, debug=True)  # host='0.0.0.0'
