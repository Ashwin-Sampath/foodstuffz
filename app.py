import os
import util
import db
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources.user import User
from resources.stock import Stock
from dotenv import load_dotenv

# Load Environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Provide Mongo Atlas URI, stored in config file
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.json_encoder = util.MongoEncoder
db.mongo.init_app(app)
api = Api(app)

api.add_resource(User, "/user")
api.add_resource(Stock, "/stock")


@app.route("/", methods=["GET"])
def index():
    return "Welcome to my ZotHacks 2020 project!"


if __name__ == "__main__":
    app.run(debug=True)
