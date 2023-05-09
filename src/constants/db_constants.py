database_info = {
    "lga_info_database": {
        "name": "lga_info",
        "views": {
            "get_lga_info_view": "LGA/get_lga_info"
        }
    },
    "lga_info_geo_database": {
        "name": "lga_info",
        "views": {
            "get_lga_info_geo_view": "LGA/get_lga_info_geo"
        }
    },
    "twitter_database_v1": {
        "name": "twitter-data-with-location",
        "views": {
            "get_ai_loc_time_view": "AI/ai_loc_time"
        }
    },
    "twitter_database_v2": {
        "name": "twitter-data-with-location-v2",
        "views": {
            "get_lga_hour_happy_view": "Happy/only_avg_sentiment",
            "get_state_hour_happy_view": "Happy_state/state_avg_sentiment"
        }
    },
    "state_info_database": {
        "name": "state_info",
        "views": {
            "get_state_info_view": "State_info/state_info"
        }
    }
}