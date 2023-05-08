from src.constants.db_constants import database_info
from couchdb import Server, Database
from couchdb.client import Row


class CouchDbHelper(object):

    def __init__(self, couchdb_server: Server) -> None:
        self.couchdb_server = couchdb_server

    def get_all_lga_info(self):
        lga_info_database = database_info["lga_info_database"]
        print(lga_info_database["name"])
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
                states[row.value[1]] = row.value[2]
        return suburbs, states

    def get_ai_loc_time(self):
        lga_info_geo_database = database_info["lga_info_geo_database"]
        print(lga_info_geo_database["name"])
        db_lga = self.couchdb_server[lga_info_geo_database["name"]]

        all_lga_info_geo_view = lga_info_geo_database["views"]["get_lga_info_geo_view"]
        print(all_lga_info_geo_view)

        ai_loc_time_database = database_info["ai_loc_time_database"]
        print(ai_loc_time_database["name"])
        db_ai = self.couchdb_server[ai_loc_time_database["name"]]

        all_ai_loc_time_view = ai_loc_time_database["views"]["get_ai_loc_time_view"]
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

    def get_lga_happy_hour(self):
        lga_hour_happy_database = database_info["lga_hour_happy_database"]
        print(lga_hour_happy_database["name"])
        db_happy_hour = self.couchdb_server[lga_hour_happy_database["name"]]
        all_lga_hour_happy_view = lga_hour_happy_database["views"]["get_lga_hour_happy_view"]

        lga_info_geo_database = database_info["lga_info_geo_database"]
        print(lga_info_geo_database["name"])
        db_lga = self.couchdb_server[lga_info_geo_database["name"]]
        all_lga_info_geo_view = lga_info_geo_database["views"]["get_lga_info_geo_view"]
        location_dict = {}
        merge_list = []

        for row in db_lga.iterview(all_lga_info_geo_view, batch=1000):
            location_dict[row.key] = [row.value[0], row.value[4]]

        for row in db_happy_hour.iterview(all_lga_hour_happy_view, batch=1000, reduce=True, group=True):
            merged_doc = {
                    **location_dict[row.key][1],
                    "properties": {
                        "name": location_dict[row.key][0],
                        "sentiment": {**row["value"]}
                    }
            }
            merge_list.append(merged_doc)

        return merge_list





