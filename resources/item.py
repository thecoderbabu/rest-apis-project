
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import items, stores
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operation on items")



@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found.")

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}
        # try:
        #     del items[item_id]
        #     return {"message": "Items deleted."}
        # except KeyError:
        #     abort(404, message="Item not found.")


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
        raise NotImplementedError("Deleting an item that is not implemented")
        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")
        # try:
        #     item = items[item_id]
        #     item |= item_data
        #     return item
        # except KeyError:
        #     abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
        # return {"items": list(items.values())}
        # return items.values()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        # item_data = request.get_json()
        # if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
        #     abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload")
        
        # for item in items.values():
        #     if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
        #         abort(400, message="Item already exists.")
        # if item_data["store_id"] not in stores:
        #     abort(404, message="Store not found.")
        # item_id = uuid.uuid4().hex
        # item = {**item_data, "id": item_id}
        # items[item_id] = item
        return item, 201
