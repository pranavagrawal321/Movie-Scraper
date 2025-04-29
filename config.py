SITES_LIST = {
    "pvr": {
        "PREFIX": "https://api3.pvrcinemas.com/api/v1/",
        "METHOD": "POST",
        "URL": {
            "cities": {
                "MASTER": "booking/content/city",
                "PAYLOAD": {
                    "lat": "0",
                    "lng": "0"
                },
                "HEADERS": {
                    'appversion': '1.0',
                    'chain': 'PVR',
                    'city': 'Delhi-NCR',
                    'platform': 'APP',
                    'Content-Type': 'application/json',
                    'Cookie': 'ak_bmsc=D8063EC1C419024CFF6874914B1A2EB5~000000000000000000000000000000~YAAQF3BWuKgnXkuWAQAARQ8odxuH/5yzK0RKVqyt6RFcUI3GKhN5TwMgF5MVG+Bsku53V4R4xKequLJhQD9BAVTQ2edDaZlpzMnha+xqORQ5GkjS3XVhXOtWnoHdSY9qRdTVOZiR4KSS+YgGD7gzEMNQIXO7gX8ev3Icl9B2dw4mJhLyaYYK0HJ9OjQgOmakEDTDs6X9RW7J/5SSXJpl9r3FWTbuFVQ4nNeVDZBq4Tv7qSFK8p7NBBXFSgvrr2XJ/w1u/NtGQ0PXlvx3TQm6bFRO/ZSyOqAMnuAI5BUtu7UIH9n8eVOErIDVau2UcQCo8U9O2/ARUTZv6g0N8/AW8EjRTF1/03VWJtrDkRuBYpo=; bm_sv=6444D261EE4222FFBAC69BB505DB136B~YAAQF3BWuFmUXkuWAQAAb8srdxs3n60wjN2/ssgP8GxAqymObUhAR+n4/2jpUK9s6aofHLNym4uB3wk8T52PYZ9GAsv4/9XEMQvn4tFLZQQ7dIS6l3kuL0LArk2yqsUuwy2i3jO6RRwcWbtzIllb4DBpgrE6R6chs6krjvK+Tc50rUT2mtZHUIvdoJ0iME1WCS9YjJBbpPIZF1BwvEaYGbT+lK9ApBabltp/y8baqJuaGVfhgUKtR5uEeGO82paeoj+J3w==~1'
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
                            },
                            "BOTH": True
                        }
                    }
                }
            },
        }
    }
}
