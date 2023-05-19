from src.constants.db_constants import database_info
from couchdb import Server, Database
from couchdb.client import Row
from uuid import uuid4
from datetime import datetime

class CouchDbHelper(object):

    def __init__(self, couchdb_server: Server) -> None:
        self.couchdb_server = couchdb_server

    def get_all_lga_info(self):
        lga_info_database = database_info["lga_info_database"]
        db = self.couchdb_server[lga_info_database["name"]]

        all_lga_info_view = lga_info_database["views"]["get_lga_info_view"]
        row: Row
        suburbs = {}
        states = {}
        for row in db.iterview(all_lga_info_view, batch=1000):
            suburbs[row.key] = {
                "name": row.value[0],
                "state_id": row.value[1]
            }
            if row.value[1] not in states:
                states[row.value[1]] = {
                    "name": row.value[2]
                }
        return suburbs, states

    def get_ai_loc_time(self):
        lga_info_geo_database = database_info["lga_info_geo_database"]
        print(lga_info_geo_database["name"])
        db_lga = self.couchdb_server[lga_info_geo_database["name"]]

        all_lga_info_geo_view = lga_info_geo_database["views"]["get_lga_info_geo_view"]
        print(all_lga_info_geo_view)

        twitter_v1_database = database_info["twitter_database_v1"]
        print(twitter_v1_database["name"])
        db_ai = self.couchdb_server[twitter_v1_database["name"]]

        all_ai_loc_time_view = twitter_v1_database["views"]["get_ai_loc_time_view"]
        row: Row
        location_dict = {}
        features = []
        for row in db_lga.iterview(all_lga_info_geo_view, batch=1000):
            location_dict[row.key] = [row.value[0], row.value[3]['lon'], row.value[3]['lat']]
        for row in db_ai.iterview(all_ai_loc_time_view, batch=1000):
            time_key = row.key
            time_value = row.value
            feature = {
                'type': 'Feature',
                "geometry": {
                    'type': 'Point',
                    "coordinates":
                        [
                            location_dict[time_key][1],
                            location_dict[time_key][2]
                        ]
                },
                'properties': {
                    'suburb': location_dict[time_key][0],
                    "timestamp": time_value
                }
            }
            features.append(feature)
        return features

    def get_lga_happy_hour(self, need_loc=True):
        lga_hour_happy_database = database_info["twitter_database_v2"]
        print(lga_hour_happy_database["name"])
        db_happy_hour = self.couchdb_server[lga_hour_happy_database["name"]]
        all_lga_hour_happy_view = lga_hour_happy_database["views"]["get_lga_hour_happy_view"]

        lga_info_geo_database = database_info["lga_info_geo_database"]
        print(lga_info_geo_database["name"])
        db_lga = self.couchdb_server[lga_info_geo_database["name"]]
        all_lga_info_geo_view = lga_info_geo_database["views"]["get_lga_info_geo_view"]
        location_dict = {}
        merge_list = []

        if need_loc:
            for row in db_lga.iterview(all_lga_info_geo_view, batch=1000,):
                location_dict[row.key] = [row.value[0], row.value[4]]
        
        for row in db_happy_hour.iterview(all_lga_hour_happy_view, batch=1000, limit=1000, reduce=True, group=True):
            if need_loc:
                merged_doc = {
                        **location_dict[row.key][1],
                        "properties": {
                            "name": location_dict[row.key][0],
                            "sentiment": {**row["value"]}
                        }
                }
            else:
                merged_doc = {
                    "lga_code": row.key,
                    "sentiment": {**row["value"]}
                }
            merge_list.append(merged_doc)

        return merge_list

    def get_state_happy_hour(self):

        state_info_database = database_info["state_info_database"]
        print(state_info_database["name"])
        db_state = self.couchdb_server[state_info_database["name"]]
        all_state_info_view = state_info_database["views"]["get_state_info_view"]



        state_hour_happy_database = database_info["twitter_database_v2"]
        print(state_hour_happy_database["name"])
        db_happy_hour = self.couchdb_server[state_hour_happy_database["name"]]
        all_state_hour_happy_view = state_hour_happy_database["views"]["get_state_hour_happy_view"]

        merge_list = []
        senti_list = {}
        for seti in db_happy_hour.iterview(all_state_hour_happy_view, batch=1000, reduce=True, group=True):
            senti_list[seti.key] = seti.value

        for row in db_state.iterview(all_state_info_view, batch=1000):
            row.value['properties']['sentiment'] = senti_list[row.key]
            merge_list.append(row.value)

        return merge_list

    def get_AI_tweets_count(self, state_code=None, top=None):
        twitter_database = database_info["twitter_database_v2"]
        db = self.couchdb_server[twitter_database["name"]]

        query_parameters = {
            "reduce": True
        }
        if state_code:
            query_parameters["group_level"] = 2
        else:
            query_parameters["group_level"] = 1

        ai_count_view = twitter_database["views"]["get_ai_tweets_count"]
        row: Row
        data = {}
        for row in db.iterview(ai_count_view, batch=1000, wrapper=CouchDbHelper._row_wrapper, **query_parameters):
            if not state_code:
                data[row["key"][0]] = row["value"]
            elif state_code == row["key"][0] and row["key"][1] != "0":
                data[str(row["key"])] = row["value"]
        sorted_ai_count = sorted(data.items(), key=lambda x:x[1], reverse=True)
        if top:
            sorted_ai_count = sorted_ai_count[:top]
        sorted_ai_count = dict(sorted_ai_count)
        return sorted_ai_count

    def get_sudo_location_info(self, state_codes, lga_codes):
        sudo_other_data_raw_database = database_info["sudo_other_data_raw_database"]
        db = self.couchdb_server[sudo_other_data_raw_database["name"]]

        data_sum_view = sudo_other_data_raw_database["views"]["data_sum"]

        state_data = {}
        lga_data = {}
        row: Row
        if len(state_codes) > 0:
            for row in db.iterview(data_sum_view, batch=1000, wrapper=CouchDbHelper._row_wrapper, reduce=True, group_level=1):
                if row["key"][0] in state_codes:
                    state_data[row["key"][0]] = row["value"]
        if len(lga_codes) > 0:
            for row in db.iterview(data_sum_view, batch=1000, wrapper=CouchDbHelper._row_wrapper, reduce=True, group_level=2):
                if row["key"][1] in lga_codes:
                    lga_data[row["key"][1]] = row["value"]
        return state_data, lga_data

    def get_AI_lang_count(self, state_codes, lga_codes):
        twitter_database = database_info["twitter_database_v2"]
        db = self.couchdb_server[twitter_database["name"]]

        ai_lang_count_view = twitter_database["views"]["get_ai_lang_count"]

        state_data = {}
        lga_data = {}
        row: Row
        if len(state_codes) > 0:
            for row in db.iterview(ai_lang_count_view, batch=1000, wrapper=CouchDbHelper._row_wrapper, reduce=True, group_level=1):
                if len(state_codes) == 0:
                    state_data[row["key"][0]] = row["value"]
                elif row["key"][0] in state_codes:
                    state_data[row["key"][0]] = row["value"]
        if len(lga_codes) > 0:
            for row in db.iterview(ai_lang_count_view, batch=1000, wrapper=CouchDbHelper._row_wrapper, reduce=True, group_level=2):
                if len(lga_codes) == 0:
                    lga_data[row["key"][1]] = row["value"]
                elif row["key"][1] in lga_codes:
                    lga_data[row["key"][1]] = row["value"]
        return state_data, lga_data

    def get_Mastodon_timeline(self):

        mastodon_database = database_info["mastodon_database"]
        print(mastodon_database["name"])
        db = self.couchdb_server[mastodon_database["name"]]
        mastodon_timeline_view = mastodon_database["views"]["get_mastodon_timeline_view"]

        result  = []


        for row in db.iterview(mastodon_timeline_view, batch=1000, reduce= True, group= True):
            my_date = datetime(2023,5,8)
            current = datetime.strptime(row.key,"%Y-%m-%d")
            if current > my_date:
                time_count = {}
                time_count['time'] = row.key
                time_count['count'] = row.value
                result.append(time_count)

        return result


    def get_Mastodon_keywords(self):

        mastodon_database = database_info["mastodon_database"]
        db = self.couchdb_server[mastodon_database["name"]]
        mastodon_keywords_view = mastodon_database["views"]["get_mastodon_keywords_view"]

        result = []

        for row in db.iterview(mastodon_keywords_view, batch=1000, reduce=True, group=True):

            name_value = {}
            name_value['name'] = row.key
            name_value['value'] = row.value
            result.append(name_value)
        
        result = sorted(result, key=lambda x: x['value'], reverse=True)
        final = result[:5]

        final.append({'name':'others', 'value':0})

        for other in result[5:]:
            final[-1]['value'] += other['value']
        

        return final


    def get_Kpop_all_group(self):

        twitter_database = database_info["twitter_database_v2"]
        db = self.couchdb_server[twitter_database["name"]]
        kpop_all_group_view = twitter_database["views"]["get_kpop_all_group_view"]

        result  = []

        for row in db.iterview(kpop_all_group_view, batch=1000,reduce=True, group=True):
            name_count =  {}
            name_count['name'] = row.key
            name_count['count'] = row.value
            result.append(name_count)
        
        result = sorted(result, key=lambda x: x['count'], reverse=True)
        final = result[:5]

        final.append({'name':'others', 'count':0})

        for other in result[5:]:
            final[-1]['count'] += other['count']

        return final


    def get_Kpop_boy_girl(self):

        state_info_database = database_info["state_info_database"]
        db_state = self.couchdb_server[state_info_database["name"]]
        all_state_info_view = state_info_database["views"]["get_state_info_view"]


        state_kpop_database = database_info["twitter_database_v2"]
        db_kpop = self.couchdb_server[state_kpop_database["name"]]
        #print(db_kpop)
        kpop_boy_girl_view = state_kpop_database["views"]["get_kpop_boy_gril_view"]

        result = []
        kpop_list = {}
        for state in db_kpop.iterview(kpop_boy_girl_view, batch=1000, reduce=True, group=True):
            kpop_list[state.key] = state.value

        for row in db_state.iterview(all_state_info_view, batch=1000):
            state_name = row.value['properties']['state_name']
            state_code = row.value['properties']['state_code']

            if state_code in kpop_list:
                name_value = {'name': state_name,
                            'value': kpop_list[state_code]
                            }
                result.append(name_value)

        return result
    
    def get_australia_sentiment_info_per_hour(self):
        twitter_database = database_info["twitter_database_v2"]
        db = self.couchdb_server[twitter_database["name"]]
        australia_sentiment_info_per_hour_view = twitter_database["views"]["get_australia_sentiment_info_per_hour"]

        row: Row
        results = []
        for row in db.iterview(australia_sentiment_info_per_hour_view, batch=1000, wrapper=CouchDbHelper._row_wrapper, reduce=True, group=True):
            results.append({
                "time": row["key"],
                "value": row["value"]["sum"] / row["value"]["count"]
            })
        return results
    
    def get_top_lga_per_state(self):
        twitter_database = database_info["twitter_database_v2"]
        db = self.couchdb_server[twitter_database["name"]]
        lga_sentiment = twitter_database["views"]["get_top_lga_sentiment"]

        state_lga = {}
        for row in db.iterview(lga_sentiment, batch=1000, wrapper=CouchDbHelper._row_wrapper, reduce=True, group_level=2):
            if int(row["key"][1]) == 0:
                continue 
            if row["key"][0] not in state_lga:
                state_lga[row["key"][0]] = [{
                    "lga_code": row["key"][1],
                    "sentiment": row["value"]["sentiment_all"] / row["value"]["num"]
                }]
            else:
                state_lga[row["key"][0]].append({
                    "lga_code": row["key"][1],
                    "sentiment": row["value"]["sentiment_all"] / row["value"]["num"]
                })
        
        top_lga_per_state = []
        for state in state_lga:
            max = -10000
            max_index = -1
            for index, lga_sentiment in enumerate(state_lga[state]):
                if lga_sentiment["sentiment"] > max:
                    max = lga_sentiment["sentiment"]
                    max_index = index
            top_lga_per_state.append({
                "state_code": state,
                "lga_code": state_lga[state][max_index]["lga_code"],
                "sentiment": state_lga[state][max_index]["sentiment"]
            })
        return top_lga_per_state


    @staticmethod
    def _row_wrapper(row: Row):
        if "id" not in row:
            row["id"] = str(uuid4())
        return row
