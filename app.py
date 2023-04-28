from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)


@app.route("/api/v1/hello", methods=['get'])
@cross_origin()
def hello():
    response = jsonify(message="Simple server is running")
    return response
