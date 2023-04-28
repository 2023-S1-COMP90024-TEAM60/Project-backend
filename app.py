from flask import Flask, g, jsonify
from flask_cors import CORS
import couchdb

admin = 'admin'
password = 'comp90024-60'
url = f'http://{admin}:{password}@172.26.129.169:5984/'
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


@app.route('/api/v1/docs/<doc_id>', methods=['get'])
def api_0(doc_id):
    # Mango Queries
    query = {
        'selector': {
            '_id': doc_id
        }
    }
    # Execute the query
    results = []
    for row in db.find(query):
        results.append(row)
    # Return the results as JSON
    return {'data': results}


if __name__ == "__main__":
    app.run(port=8000)
