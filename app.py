from flask import Flask, g, jsonify, request
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




@app.route("/AI/aiData", methods=['get'])
def get_map_data():
    features = couchdb_helper.get_ai_loc_time()
    data = {
        'type': 'FeatureCollection',
        'features': features
    }
    return jsonify(data)


@app.route("/LGA/sentimentData", methods=['get'])
def get_LGA_happy_data():
    args = request.args
    need_loc_param= args.get("need_loc")
    need_loc = True
    if need_loc_param == "false":
        need_loc = False
    merge_list = couchdb_helper.get_lga_happy_hour(need_loc=need_loc)
    data = {
            'type': 'FeatureCollection',
            'features': merge_list
        }
    return jsonify(data)



@app.route("/STATE/sentimentData", methods=['get'])
def get_happy_data():
    merge_list = couchdb_helper.get_state_happy_hour()
    data = {
            'type': 'FeatureCollection',
            'features': merge_list
        }
    return jsonify(data)


@app.route("/LGA/lgaInfo", methods=['get'])
def get_all_lga_info():
    suburbs, states = couchdb_helper.get_all_lga_info()
    data = {
        "suburbs": suburbs,
        "states": states
    }
    return jsonify(data)

@app.route("/AI/tweetsCount", methods=['get'])
def get_ai_tweets_count():
    args = request.args
    state_code = args.get("state_code")
    top = args.get("top")
    if top:
        top = int(top)
    ai_count_data = couchdb_helper.get_AI_tweets_count(state_code, top)
    return_payload = {
        "ai_count": ai_count_data
    }
    return jsonify(return_payload)

@app.route("/AI/langCount", methods=['get'])
def get_ai_lang_count():
    args = request.args
    state_codes = args.getlist("state_codes")
    lga_codes = args.getlist("lga_codes")
    state_data, lga_data = couchdb_helper.get_AI_lang_count(state_codes, lga_codes)
    return_payload = {
        "state_data": state_data,
        "lga_data": lga_data
    }
    return jsonify(return_payload)

@app.route("/sudo/locationsInfo", methods=['get'])
def get_sudo_locations_info():
    args = request.args
    state_codes = args.getlist("state_codes")
    lga_codes = args.getlist("lga_codes")
    state_data, lga_data = couchdb_helper.get_sudo_location_info(state_codes, lga_codes)

    return_payload = {
        "state_data": state_data,
        "lga_data": lga_data
    }
    return jsonify(return_payload)

@app.route("/Mastodon/timeline", methods=['get'])
def get_mastodon_timeline():
    data = couchdb_helper.get_Mastodon_timeline()
    return jsonify(data)

@app.route("/Mastodon/keywords", methods=['get'])
def get_mastodon_keywords():
    data = couchdb_helper.get_Mastodon_keywords()
    return jsonify(data)

@app.route("/Kpop/allGroup", methods=['get'])
def get_kpop_all_group():
    data = couchdb_helper.get_Kpop_all_group()
    return jsonify(data)

@app.route("/Kpop/boyGirl", methods=['get'])
def get_kpop_boy_girl():
    data = couchdb_helper.get_Kpop_boy_girl()
    return jsonify(data)

@app.route("/Sentiment/timeline", methods=['get'])
def get_sentiment_timeline():
    results = couchdb_helper.get_australia_sentiment_info_per_hour()
    return jsonify(results)

@app.route("/Sentiment/topLgaPerState", methods=['get'])
def get_top_lga_sentiment():
    results = couchdb_helper.get_top_lga_per_state()
    return jsonify(results)

@app.route("/Covid/twitter", methods=['get'])
def get_covid_twitter():
    data = couchdb_helper.get_Covid_twitter()
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=8000)
