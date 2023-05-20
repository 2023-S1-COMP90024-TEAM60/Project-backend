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
    "twitter_database_v2": {
        "name": "twitter-data-with-location-v2",
        "views": {
            "get_lga_hour_happy_view": "Happy/only_avg_sentiment",
            "get_state_hour_happy_view": "Happy_state/state_avg_sentiment",
            "get_ai_tweets_count": "AI_count/count",
            "get_ai_lang_count": "AI_Language/lang",
            "get_kpop_boy_gril_view": "Kpop/count_group_term",
            "get_kpop_all_group_view": "Kpop_term/term_count",
            "get_australia_sentiment_info_per_hour": "Happy/each_hour_info",
            "get_top_lga_sentiment": "Happy_lga/state_lga",
            "get_ai_loc_time_view": "AI/ai_lga_time",
            "get_covid_twitter":"Covid/covid_term_twitter"
        }
    },
    "sudo_other_data_raw_database": {
        "name": "sudo_other_data_raw",
        "views": {
            "data_sum": "sudo_other_data/sum",
        }
    },
    "state_info_database": {
        "name": "state_info",
        "views": {
            "get_state_info_view": "State_info/state_info"
        }
    },
    "mastodon_database": {
        "name": "mastodon",
        "views": {
            "get_mastodon_timeline_view": "covid_timeline/covid_count_all",
            "get_mastodon_keywords_view": "covid_term/term_count"
        }
    }
}