from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from security import UserLogin, UserRegister

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
api = Api(app)

jwt = JWTManager(app)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float,
        required=True,
        help="This field can not be left blank"
    )

    @jwt_required()
    def get(self, name):
        # if no item found return None
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': f'An item with name {name} already exists.'}, 400

        # data = request.get_json()  # force=True, silent=True
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)

        return item, 201

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = next(filter(lambda item: item['name'] == name, items), None)

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))

        return {'message': 'Item deleted'}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}, 200

    @jwt_required()
    def post(self, name):
        item = {'name': name, 'price': 14}
        items.append(item)

        return item, 201


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')

app.run(port=4242, debug=True)  # host='0.0.0.0'
