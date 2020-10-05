import json
from bson.objectid import ObjectId


class MongoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def get_mongo_query(params):
    query = {}
    for key, value in params.items():
        # Converts "_id" to Mongo ObjectId for querying
        if key == "_id" and value:
            query[key] = ObjectId(value)
        elif value:
            query[key] = value
    return query
