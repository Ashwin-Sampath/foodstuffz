from flask import Flask, json, request
from flask_cors import CORS
from flask_restful import Api
#from resources.user import User
from dotenv import load_dotenv
from credentials import id, key

# Load Environment variables
load_dotenv()

app = Flask(__name__)
# Allow cross domain apps to access API
CORS(app)
api = Api(app)


# Vanilla Flask route
@app.route("/", methods=["GET"])
def index():
    return "Welcome to my ZotHacks 2020 project!"


# Handles validation errors and returns JSON Object
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return json.jsonify({"errors": messages}), err.code


@app.route("/search")
def search():
    #Base url to add to
    URL = "https://api.edamam.com/search?"

    #request.args is a dict that contains the search parameters
    args = request.args

    if len(args) != 0:
        #adds query text to url
        if 'q' in args:
            URL += 'q=' + args['q'] + '&'
        else:
            return "invalid search"
        
        #Adds id and key to request so it can be authenticated by the Edamam API
        URL += "app_id=" + id + '&'
        URL += "app_key=" + key

        response = requests.get(URL).json()

        #Not sure if I just return the response or do something else    

        
    else:
        #Also not sure if returning just this is ok or if something else is needed
        return "Empty search"


if __name__ == "__main__":
    app.run(debug=True)
