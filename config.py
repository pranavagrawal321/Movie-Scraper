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
                    "PARENT": "movieCinemaSessions,experienceSessions,shows",
                    "FIELD_KEYS": {
                        "KEY": "seat_id",
                        "VALUE": "encrypted"
                    }
                }
            }
        }
    }
}
