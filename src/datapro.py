import requests
import couchdb
import json
from itertools import groupby

admin = 'admin'
password = 'comp90024-60'
url = f'http://{admin}:{password}@172.26.136.78:5984/'
couch = couchdb.Server(url)


def ai_loc_time():
    location_db_name = 'lga_info'
    location_view_name = 'LGA/_view/get_lga_info_geo'
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
                    'properties': {
                                   'surburb': suburb_name,
                                   "timestamp": time_value
                                   }
                }
                features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    return geojson


def happy_lga_time():
    r1 = requests.get(url + "/" + "lga_info" + "/_design/LGA/_view/get_lga_info_geo")
    docs1 = r1.json()["rows"]
    r2 = requests.get(url + "/" + "test" + "/_design/general_happy/_view/only_sentiment?Reduced%20=true&group_level=1")
    docs2 = r2.json()["rows"]
    mergelist = []
    for doc1 in docs1:
        doc_id = doc1["key"]
        doc_value = doc1["value"]
        for doc2 in docs2:
            if doc2["key"] == doc_id:
                merged_doc = { **doc1["value"][4],
                               "properties": {
                                    "name": doc1["value"][0],
                                    "sentiment": {**doc2["value"]}
                               },
                               }
                mergelist.append(merged_doc)
                break
    merged_docs = {
            'type': 'FeatureCollection',
            'features': mergelist
            }
    return merged_docs


# @app.route("/LGA/Happy", methods=['get'])
# def happy():
#     try:
#         location_db_name = 'lga_info'
#         location_view_name = 'LGA/_view/get_lga_info_geo'
#         location_response = requests.get(url + location_db_name + '/_design/' + location_view_name)
#         location_data = location_response.json()['rows']
#
#         # time_db_name = 'twitter-data-with-location'
#         # time_view_name = 'Happy/_view/lga_sentiment'
#         # params = {'Reduce': 'true', 'group_level': '1'}
#         # time_response = requests.get(url + time_db_name + '/_design/' + time_view_name, params)
#         # time_data = time_response.json()['rows']
#
#         features = []
#         for item in location_data:
#             #key = item['key']
#             type = item['value'][4]["geometry"]["type"]
#             coordinates = item['value'][4]["geometry"]["coordinates"]
#
#             feature = {
#                 'type': 'Feature',
#                 "geometry": {
#                     'type': type,
#                     "coordinates": coordinates
#                 },
#
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


# hour_transfer = {
#     0: "0-1",
#     1: "1-2",
#     2: "2-3",
#     3: "3-4",
#     4: "4-5",
#     5: "5-6",
#     6: "6-7",
#     7: "7-8",
#     8: "8-9",
#     9: "9-10",
#     10: "10-11",
#     11: "11-12",
#     12: "12-13",
#     13: "13-14",
#     14: "14-15",
#     15: "15-16",
#     16: "16-17",
#     17: "17-18",
#     18: "18-19",
#     19: "19-20",
#     20: "20-21",
#     21: "21-22",
#     22: "22-23",
#     23: "23-24"
# }

# def happy_lga_time():
#     view_name = '_design/LGA/_view/get_lga_info_geo'
#     db = couch['lga_info']
#     time_db_name = 'test'
#     time_view_name = 'general_happy/_view/only_sentiment'
#     params = {'Reduce%20': 'true', 'group_level': '1'}
#     time_response = requests.get(url + time_db_name + '/_design/' + time_view_name, params)
#     time_data = time_response.json()['rows']
#     features = []
#     for item in db.iterview(view_name, 1000, wrapper=None):
#         key = item['key']
#         suburb_name = item['value'][0]
#         properties = {}
#         for time_item in time_data:
#             time_key = time_item['key']
#
#             if key == time_key:
#                 #print("1111")
#                 properties = {
#                     "name": suburb_name,
#                     "sentiment": time_item['value']
#                 }
#             feature = {
#                 'type': 'Feature',
#                 "properties": dict(properties),
#                 "geometry": item['value'][4]["geometry"]
#             }
#
#             #print(feature)
#
#             features.append(feature)
#
#     geojson = {
#         'type': 'FeatureCollection',
#         'features': features
#     }
#     with open("data.geojson", "w") as f:
#         json.dump(geojson, f)
#     return geojson
#
# happy_lga_time()
