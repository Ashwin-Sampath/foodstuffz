from flask import json
from flask_restful import Resource
from bson.objectid import ObjectId
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from db import mongo


class GetSchema(Schema):
    # Convert str to Mongo Object ID
    _id = fields.Function(deserialize=lambda obj: ObjectId(obj))
    email = fields.Email()
    firstName = fields.Str()
    lastName = fields.Str()
    favoriteCompany = fields.Str()


class PostSchema(Schema):
    email = fields.Email(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    favoriteCompany = fields.Str()


class PutQuerySchema(Schema):
    _id = fields.Function(deserialize=lambda obj: ObjectId(obj), required=True)


class PutBodySchema(Schema):
    email = fields.Email(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    favoriteCompany = fields.Str()


class DeleteSchema(Schema):
    _id = fields.Function(deserialize=lambda obj: ObjectId(obj), required=True)


class User(Resource):
    @use_args(GetSchema(), location="querystring")
    def get(self, query):
        # Search for all users that match query arguments
        users = [user for user in mongo.db.user.find(query)]
        return json.jsonify(data=users)

    @use_args(PostSchema(), location="json")
    def post(self, body):
        # Create user with data from request
        mongo.db.user.insert_one(body)
        return json.jsonify(data=body)

    @use_args(PutQuerySchema(), location="querystring")
    @use_args(PutBodySchema(), location="json")
    def put(self, query, body):
        user_id = query.get("_id")
        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"message": "User not found"}, 404
        # Update user with data from request
        mongo.db.user.update_one({"_id": ObjectId(user_id)}, {"$set": body})
        updated_user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        return json.jsonify(data=updated_user)

    @use_args(DeleteSchema(), location="querystring")
    def delete(self, query):
        user_id = query.get("_id")
        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"message": "User not found"}, 404
        # Delete user based on _id
        mongo.db.user.delete_one({"_id": ObjectId(user_id)})
        return {"message": "User was deleted"}
