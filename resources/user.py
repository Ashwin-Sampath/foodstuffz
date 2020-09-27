from flask import json
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from db import mongo

# Parameter parser used for GET request
search_params = reqparse.RequestParser()
search_params.add_argument("_id", type=str)
search_params.add_argument("email", type=str)
search_params.add_argument("firstName", type=str)
search_params.add_argument("lastName", type=str)

# Parameter parser used for PUT and DELETE requests
required_id = reqparse.RequestParser()
required_id.add_argument("_id", type=str, required=True, help="Id cannot be missing")

# Body parser used for POST and PUT requests
required_body = reqparse.RequestParser()
required_body.add_argument(
    "email", type=str, required=True, help="Email cannot be missing"
)
required_body.add_argument(
    "firstName", type=str, required=True, help="First name cannot be missing"
)
required_body.add_argument(
    "lastName", type=str, required=True, help="Last name cannot be missing"
)


class User(Resource):
    def get(self):
        params = search_params.parse_args()
        query = {}
        for key, value in params.items():
            # Converts "_id" to Mongo ObjectId for querying
            if key == '_id' and value:
                query[key] = ObjectId(value)
            elif value:
                query[key] = value
        if not query:
            return {"message": "Invalid params"}, 400
        # Search for all users that match query parameters
        users = [user for user in mongo.db.user.find(query)]
        if not users:
            return {"message": "User not found"}, 404
        return json.jsonify(users)

    def post(self):
        data = required_body.parse_args()
        # Create user with data from request
        mongo.db.user.insert_one(data)
        return json.jsonify(data)

    def put(self):
        params = required_id.parse_args()
        user_id = params.get("_id")
        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"message": "User not found"}, 404
        data = required_body.parse_args()
        # Update user with data from request
        mongo.db.user.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        updated_user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        return json.jsonify(updated_user)

    def delete(self):
        params = required_id.parse_args()
        user_id = params.get("_id")
        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"message": "User not found"}, 404
        # Delete user based on _id
        mongo.db.user.delete_one({"_id": ObjectId(user_id)})
        return {"message": "User was deleted"}
