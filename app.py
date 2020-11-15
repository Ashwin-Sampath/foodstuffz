from flask import Flask, json, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
from credentials import id, key
import requests

# Load Environment variables
load_dotenv()

app = Flask(__name__)
# Allow cross domain apps to access API
CORS(app)
api = Api(app)



# Handles validation errors and returns JSON Object
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return json.jsonify({"errors": messages}), err.code


@app.route("/search", methods = ["GET", "POST"])
def search():
    #Base url to add to
    URL = "https://api.edamam.com/search?"

    #Parses the request data and converts into string
    content = request.get_json()
    ingredients = content["ingredients"]
    healthLabels = content["healthLabels"]
    
    

    if ingredients:
        #adds query text to url
        queryIngredientStr = ','.join(ingredients)
        URL += 'q=' + queryIngredientStr + '&'

        #adds optional health labels to url if they exist
        if healthLabels:
            for elem in healthLabels:
                URL += 'health=' + elem + '&'
        
        #adds id and key to request so it can be authenticated by the Edamam API
        URL += "app_id=" + id + '&'
        URL += "app_key=" + key

        #sends url request to API and stores in a request object converted into a JSON object
        response = requests.get(URL).json()

        #(Hopefully) recipes is a list of 'hit' objects, each of which is a dictionary
        recipes = response['hits']

        return jsonify( {'label': recipes[0]['recipe']['label']} )
        
    else:
        return "Empty search", 404



if __name__ == "__main__":
    app.run()
