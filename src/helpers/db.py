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
