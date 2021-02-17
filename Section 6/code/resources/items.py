import sqlite3
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float,
        required=True,
        help="This field can not be left blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.toJson()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        # data = request.get_json()  # force=True, silent=True
        data = Item.parser.parse_args()
        item = ItemModel(None, name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error occured'}, 500

        return item.toJson(), 201

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(None, name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occured while adding item'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occured while updating item'}, 500

        return updated_item.toJson(), 201

    @jwt_required()
    def delete(self, name):
        ItemModel(None, name, None).delete()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    @classmethod
    def get_items(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT name,price FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return items

    @jwt_required()
    def get(self):
        return {'items': self.get_items()}, 200

    @jwt_required()
    def post(self, name):
        item = {'name': name, 'price': 14}
        """ items.append(item) """

        return item, 201
