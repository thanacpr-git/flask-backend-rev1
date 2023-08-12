# running flask option 
# python -m flask run --host=0.0.0.0 --port=80
import re
from datetime import datetime

from flask import Flask, jsonify
from flask_restx import Api, Resource
import requests
import json

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

@api.route('/contents/<string:topic>')
class SearchContents(Resource):
    def get(self, topic):
        url = 'https://hn.algolia.com/api/v1/search?query=' + topic
        response = requests.get(url)
        data = []
        if(response.status_code == 200):
            raw_data = json.loads(response.text)
            for index in raw_data['hits']:
                if index['title'] and index['url']:
                    data.append({
                        'id': index['objectID'],
                        'title' : index['title'],
                        'url': index['url']
                    })
        
        response = jsonify(outcome=data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        
        return response
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')