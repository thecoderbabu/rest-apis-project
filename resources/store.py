import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import stores

from db import db
from models import StoreModel
from schemas import StoreSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
blp = Blueprint("stores", __name__, description="Operation on stores")



@blp.route("/store/<int:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}
        # raise NotImplementedError("Deleting an item that is not implemented")

        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        # return {"stores": list(stores.values())}
        # return stores.values()

    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.") 
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store
        return store, 201
