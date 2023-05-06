from flask import Flask, g, jsonify
from flask_cors import CORS
import couchdb
from src.datapro import ai_loc_time, happy_lga_time

admin = 'admin'
password = 'comp90024-60'
url = f'http://{admin}:{password}@172.26.136.78:5984/'
couch = couchdb.Server(url)
db_name = 'testdb'

if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

app = Flask(__name__)
CORS(app)


@app.route("/api/v1/hello", methods=['get'])
def hello():
    response = jsonify(message="Simple server is running")
    return response


@app.route("/AI/mapData", methods=['get'])
def map_data():
    processed_data = ai_loc_time()
    return jsonify(processed_data)


@app.route("/LGA/Happy", methods=['get'])
def happy():
    processed_data = happy_lga_time()
    return jsonify(processed_data)





if __name__ == "__main__":
    app.run(port=8000)
