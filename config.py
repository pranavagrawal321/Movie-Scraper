from datetime import date
from random import randint

SITES_LIST = {
    "pvr": {
        "PREFIX": "https://api3.pvrcinemas.com/api/v1/",
        "METHOD": "POST",
        "PROXY": "YES",
        "URL": {
            "cities": {
                "MASTER": "booking/content/city",
                "PAYLOAD": {
                    "lat": "0",
                    "lng": "0"
                },
                "HEADERS": {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en;q=0.7',
                    'appversion': '1.0',
                    'chain': 'PVR',
                    'city': 'Delhi-NCR',
                    'content-type': 'application/json',
                    'country': 'INDIA',
                    'flow': 'PVRINOX',
                    'origin': 'https://www.pvrcinemas.com',
                    'platform': 'APP',
                    'sec-gpc': '1'
                },
                "RULE_JSON": {
                    "PARENT": "output,ot",
                    "FIELD_KEYS": {
                        "KEY": "cities",
                        "VALUE": {
                            "IF": {
                                "KEY": "city",
                                "VALUE": "subcities,name"
                            },
                            "ELSE": {
                                "KEY": "city",
                                "VALUE": "name"
                            }
                        }
                    }
                }
            },
            "movies": {
                "MASTER": "booking/content/nowshowing",
                "PAYLOAD": {
                    "city": "{{cities}}"
                },
                "HEADERS": {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en;q=0.7',
                    'appversion': '1.0',
                    'chain': 'PVR',
                    'city': '{{cities}}',
                    'content-type': 'application/json',
                    'country': 'INDIA',
                    'origin': 'https://www.pvrcinemas.com',
                    'platform': 'WEBSITE',
                    'priority': 'u=1, i',
                    'sec-gpc': '1'
                },
                "RULE_JSON": {
                    "PARENT": "output,mv",
                    "FIELD_KEYS": {
                        "KEY": "movie_id",
                        "VALUE": "filmIds"
                    },
                }
            },
            "sessions": {
                "MASTER": "booking/content/msessions",
                "PAYLOAD": {
                    "city": "{{cities}}",
                    "mid": "{{movie_id}}"
                },
                "HEADERS": {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en;q=0.7',
                    'appversion': '1.0',
                    'authorization': 'Bearer',
                    'chain': 'PVR',
                    'city': "{{cities}}",
                    'content-type': 'application/json',
                    'country': 'INDIA',
                    'origin': 'https://www.pvrcinemas.com',
                    'platform': 'WEBSITE',
                    'priority': 'u=1, i',
                    'sec-gpc': '1',
                },
                "RULE_JSON": {
                    "PARENT": "output,movieCinemaSessions,experienceSessions,shows",
                    "FIELD_KEYS": {
                        "KEY": "seat_id",
                        "VALUE": "encrypted"
                    }
                }
            },
            "seats": {
                "MASTER": "booking/ticketing/seatlayout",
                "METHOD": "POST",
                "PAYLOAD": {
                    "dated": date.today().strftime("%Y-%m-%d"),
                    "encrypted": "{{encrypted_keys}}",
                    "onPage": False,
                    "layoutType": "NEW"
                },
                "HEADERS": {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en;q=0.7',
                    'appversion': '1.0',
                    'authorization': 'Bearer',
                    'chain': 'PVR',
                    'city': "{{cities}}",
                    'content-type': 'application/json',
                    'country': 'INDIA',
                    'origin': 'https://www.pvrcinemas.com',
                    'platform': 'WEBSITE',
                    'priority': 'u=1, i'
                },
                "RULE_JSON": {
                    "PARENT": "output",
                    "FIELD_KEYS": {
                        "movie_id": "filmData,filmId",
                        "movie_name": "filmData,filmNameWeb",
                        "format": "filmData,format",
                        "release_date": "filmData,releaseDate",
                        "certificate": "filmData,certificate",
                        "starring": "filmData,starring",
                        "director": "filmData,director",
                        "length": "filmData,runningTime",
                        "genre": "filmData,genre",
                        "language": "filmData,language",
                        "summary": "filmData,synopsis",
                        "secondary_genre": "filmData,secondaryGenre",
                        "trailer_1": "filmData,trailerUrl1",
                        "trailer_2": "filmData,trailerUrl2",
                        "trailer_3": "filmData,trailerUrl3",
                        "trailer_4": "filmData,trailerUrl4",
                        "subtitle_language": "filmData,subtitle",
                        "category": "filmData,category",
                        "show_category": "filmData,showCategory"
                    }
                }
            }
        }
    },
    "cinepolis": {
        "PREFIX": "https://api_new.cinepolisindia.com/api/movies/",
        "PROXY": "YES",
        "URL": {
            "cities": {
                "MASTER": "cities",
                "HEADERS": {
                    'Referer': 'https://cinepolisindia.com/',
                    'city_id': str(randint(9, 31)),
                    'Accept': 'application/json'
                },
                "RULE_JSON": {
                    "PARENT": "data",
                    "FIELD_KEYS": {
                        "KEY": "city",
                        "VALUE": "city_id"
                    }
                }
            },
            "movies": {
                "MASTER": "now-playing-filtered/?movie_language_id=&movie_genre_id=&city_id=9",
                "HEADERS": {
                    'accept': 'application/json',
                    'accept-language': 'en-GB,en;q=0.6',
                    'city_id': '9',
                    'origin': 'https://cinepolisindia.com',
                    'priority': 'u=1, i',
                    'referer': 'https://cinepolisindia.com/'
                },
                "RULE_JSON": {
                    "PARENT": "data",
                    "FIELD_KEYS": {
                        "KEY": "movie_id",
                        "VALUE": "movie_id"
                    }
                }
            }
        }
    }
}
