from flask import Flask, g, jsonify
from flask_cors import CORS
import couchdb
import requests
import json
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


# @app.route("/api/v1/mapdata", methods=['get'])
# def mapdata():
#     db_name = 'twitter-data-with-location'
#     view_name = 'AI/_view/new-view'
#     params = {'reduce': 'true'}
#     response = requests.get(url + db_name + '/_design/' + view_name, params=params)
#     if response.status_code == 200:
#         data = response.json()['rows'][0]['value']
#         return jsonify({'sum': data['sum']})
#     else:
#         return jsonify({'error': 'Failed to retrieve data from database.'})
#
# @app.route("/api/v1/multimapdata", methods=['get'])
# def multimapdata():
#     try:
#         db_name = 'twitter-data-with-location'
#         view_name = 'AI/_view/new-view'
#         params = {'reduce': 'true', 'group_level': '1'}
#         response = requests.get(url + db_name + '/_design/' + view_name, params=params)
#         data = response.json()['rows']
#         features = []
#         for item in data:
#             key = item['key']
#             count = item['value']['count']
#             sumsqr = item['value']['sumsqr']
#
#             if key:
#                 key = key.strip()  # 去除首尾空格
#
#             feature = {
#                 'type': 'Feature',
#                 'nameof': {'key': key},
#                 'properties': {'count': count, 'sumsqr': sumsqr}
#             }
#             features.append(feature)
#
#         geojson = {
#             'type': 'FeatureCollection',
#             'features': features
#         }
#
#         return jsonify(geojson)
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route("/api/v1/mapreturn", methods=['get'])
# def mapreturn():
#     try:
#         db_name = 'location'
#         view_name = 'Location/_view/extract_lga_info'
#         #params = {'reduce': 'true', 'group_level': '1'}
#         response = requests.get(url + db_name + '/_design/' + view_name)
#         data = response.json()['rows']
#         features = []
#         for item in data:
#             key = item['key']
#             lon = item['value'][3]['lon']
#             lat = item['value'][3]['lat']
#
#             if key:
#                 key = key.strip()  # 去除首尾空格
#
#             feature = {
#                 'type': 'Feature',
#                 "geometry": {
#                     'type': 'Point',
#                     "coordinates":
#                         [
#                             lon,
#                             lat
#                         ]
#                 },
#                 'properties': {'count': 0,
#                                'surburb': 1,
#                                "timestamp": 2
#                                }
#             }
#             features.append(feature)
#
#         geojson = {
#             'type': 'FeatureCollection',
#             'features': features
#         }
#
#         return jsonify(geojson)
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route("/AI/mapData", methods=['get'])
def map_data():
    try:
        location_db_name = 'location'
        location_view_name = 'Location/_view/extract_lga_info'
        location_response = requests.get(url + location_db_name + '/_design/' + location_view_name)
        location_data = location_response.json()['rows']

        time_db_name = 'twitter-data-with-location'
        time_view_name = 'AI/_view/ai_loc_time'
        time_response = requests.get(url + time_db_name + '/_design/' + time_view_name)
        time_data = time_response.json()['rows']

        features = []
        for timestamp in time_data:
            time_key = timestamp['key']
            time_value = timestamp['value']
            for item in location_data:
                key = item['key']
                suburb_name = item['value'][0]
                lon = item['value'][3]['lon']
                lat = item['value'][3]['lat']

                if time_key == key:
                    feature = {
                        'type': 'Feature',
                        "geometry": {
                            'type': 'Point',
                            "coordinates":
                                [
                                    lon,
                                    lat
                                ]
                        },
                        'properties': {'count': 1,
                                       'surburb': suburb_name,
                                       "timestamp": time_value
                                       }
                    }
                    features.append(feature)

        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }

        return jsonify(geojson)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# @app.route('/api/v1/docs/<doc_id>', methods=['get'])
# def api_0(doc_id):
#     # Mango Queries
#     query = {
#         'selector': {
#             '_id': doc_id
#         }
#     }
#     # Execute the query
#     results = []
#     for row in db.find(query):
#         results.append(row)
#     # Return the results as JSON
#     return {'data': results}


if __name__ == "__main__":
    app.run(port=8000)
