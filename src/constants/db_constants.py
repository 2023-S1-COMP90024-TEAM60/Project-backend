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
            "get_ai_tweets_count": "AI_count/count",
            "get_ai_lang_count": "AI_Language/lang"
        }
    },
    "sudo_other_data_raw_database": {
        "name": "sudo_other_data_raw",
        "views": {
            "data_sum": "sudo_other_data/sum",
        }
    }
}