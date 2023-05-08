from flask import Flask, g, jsonify
from flask_cors import CORS
import couchdb
from src.datapro import ai_loc_time, happy_lga_time
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
    mergelist = couchdb_helper.get_lga_happy_hour()
    data = {
            'type': 'FeatureCollection',
            'features': mergelist
        }
    return jsonify(data)

# @app.route("/LGA/Happy", methods=['get'])
# def happy():
#     global global_happylga
#     if global_happylga is None:
#         global_happylga = happy_lga_time()
#     return jsonify(global_happylga)


@app.route("/LGA/getAllLgaInfo", methods=['get'])
def get_all_lga_info():
    suburbs, states = couchdb_helper.get_all_lga_info()
    data = {
        "suburbs": suburbs,
        "states": states
    }
    return jsonify(data)


# def compute_data():
#     global global_happylga, global_mapdata
#     global_mapdata = ai_loc_time()
#     global_happylga = happy_lga_time()


# @app.route("/AI/mapData", methods=['get'])
# def map_data():
#     processed_data = ai_loc_time()
#     return jsonify(processed_data)


# @app.route("/LGA/Happy", methods=['get'])
# def happy():
#     processed_data = happy_lga_time()
#     return jsonify(processed_data)

# @app.route("/AI/mapData", methods=['get'])
# def map_data():
#     global global_mapdata
#     if global_mapdata is None:
#         global_mapdata = ai_loc_time()
#     return jsonify(global_mapdata)

if __name__ == "__main__":
    #compute_data()
    app.run(port=8000)
