from flask import Flask, g, jsonify
from flask_cors import CORS
import couchdb
from src.helpers.db import CouchDbHelper

admin = 'admin'
password = 'comp90024-60'
url = f'http://{admin}:{password}@172.26.136.78:5984/'
couch = couchdb.Server(url)

couchdb_helper = CouchDbHelper(couch)

app = Flask(__name__)
CORS(app)


@app.route("/api/v1/hello", methods=['get'])
def hello():
    response = jsonify(message="Simple server is running")
    return response



@app.route("/AI/getMapData", methods=['get'])
def get_map_data():
    features = couchdb_helper.get_ai_loc_time()
    data = {
        'type': 'FeatureCollection',
        'features': features
    }
    return jsonify(data)

@app.route("/LGA/Happy", methods=['get'])
def get_happy_data():
    merge_list = couchdb_helper.get_lga_happy_hour()
    data = {
            'type': 'FeatureCollection',
            'features': merge_list
        }
    return jsonify(data)


@app.route("/LGA/getAllLgaInfo", methods=['get'])
def get_all_lga_info():
    suburbs, states = couchdb_helper.get_all_lga_info()
    data = {
        "suburbs": suburbs,
        "states": states
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=8000)
