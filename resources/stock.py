import util
from flask import json
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from db import mongo

# Parameter parser used for GET request
search_params = reqparse.RequestParser()
search_params.add_argument("_id", type=str)
search_params.add_argument("companyName", type=str)
search_params.add_argument("symbol", type=str)

# Parameter parser used for PUT and DELETE requests
required_id = reqparse.RequestParser()
required_id.add_argument("_id", type=str, required=True, help="Id cannot be missing")

# Body parser used for POST and PUT requests
required_body = reqparse.RequestParser()
required_body.add_argument(
    "companyName", type=str, required=True, help="Company Name cannot be missing"
)
required_body.add_argument(
    "symbol", type=str, required=True, help="Symbol cannot be missing"
)


class Stock(Resource):
    def get(self):
        params = search_params.parse_args()
        query = util.get_mongo_query(params)
        # Search for all stocks that match query parameters
        stocks = [stock for stock in mongo.db.stock.find(query)]
        return json.jsonify(data=stocks)

    def post(self):
        data = required_body.parse_args()
        # Create stock with data from request
        mongo.db.stock.insert_one(data)
        return json.jsonify(data=data)

    def put(self):
        params = required_id.parse_args()
        stock_id = params.get("_id")
        stock = mongo.db.stock.find_one({"_id": ObjectId(stock_id)})
        if not stock:
            return {"message": "Stock not found"}, 404
        data = required_body.parse_args()
        # Update stock with data from request
        mongo.db.stock.update_one({"_id": ObjectId(stock_id)}, {"$set": data})
        updated_stock = mongo.db.stock.find_one({"_id": ObjectId(stock_id)})
        return json.jsonify(data=updated_stock)

    def delete(self):
        params = required_id.parse_args()
        stock_id = params.get("_id")
        stock = mongo.db.stock.find_one({"_id": ObjectId(stock_id)})
        if not stock:
            return {"message": "Stock not found"}, 404
        # Delete stock based on _id
        mongo.db.stock.delete_one({"_id": ObjectId(stock_id)})
        return {"message": "Stock was deleted"}
