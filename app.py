import util
import db
from flask import Flask
from flask_restful import Api
from resources.user import User


app = Flask(__name__)
# Provide Mongo Atlas URI
app.config["MONGO_URI"] = ""
app.json_encoder = util.MongoEncoder
db.mongo.init_app(app)
api = Api(app)

api.add_resource(User, "/user")


if __name__ == "__main__":
    app.run()
