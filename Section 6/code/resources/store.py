from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float,
        required=True,
        help="This field can not be left blank"
    )

    parser.add_argument(
        'store_id', type=float,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.toJson()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with name {name} already exists.'}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured'}, 500

        return store.toJson(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.toJson() for store in StoreModel.get_items()]}, 200
        """ return {'items': list(map(lambda item: item.toJson(), ItemModel.get_items()))}, 200 """
