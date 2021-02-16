import sqlite3
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float,
        required=True,
        help="This field can not be left blank"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}, 200

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?,?)"
        cursor.execute(query, (None, item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        # data = request.get_json()  # force=True, silent=True
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert_item(item)
        except:
            return {'message': 'An error occured'}, 500

        return item, 201

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert_item(updated_item)
            except:
                return {'message': 'An error occured while adding item'}, 500
        else:
            try:
                self.update_item(updated_item)
            except:
                return {'message': 'An error occured while updating item'}, 500

        return updated_item, 201

    @jwt_required()
    def delete(self, name):
        self.delete_item(name)

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
