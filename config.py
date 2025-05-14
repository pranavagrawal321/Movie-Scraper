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
                    'appversion': '1.0',
                    'city': '{{cities}}',
                    'content-type': 'application/json',
                    'platform': 'WEBSITE',
                    'Cookie': 'ak_bmsc=E2EE3980C10701E95642A19FF81AD2F1~000000000000000000000000000000~YAAQF3BWuG3i9oaWAQAAyc/GpxuDVsc1jF9IeWk1nIEEovMdCqKX7+f32uflXq6CCgu1+1rGiIFQIqQwiceY7RInHgsGn/S6tKcmi//vGraRMx01lhsnTILBchmpUFkSWWeBHvHGOiWI8qM3aEcF9MI/ASZC9vwuXy829upN5ujJpWmd9OG3IlmSVDEdQQfZtZ8ZE9pCZV+KsvsWgo9SdByDtyoJhlqYzt9+kjN0BKcAiRtxBhf+apRnkd5ZVbUpBgbpAT2GLxXRozARJerBdpPVccfsDAf4lg7mNyHg/goGe4e0gk/LbqiqEqcjVHXWpUTXy/h3DyI8KiDi0OETQfZklqVaS276ItEeyllASbQscXvfOA==; bm_sv=60501F383E5A3F5DA53982C682C40E69~YAAQF3BWuPXh9oaWAQAASqTGpxtBPT2xcecv8W91LCXbKoNepORl6r3oxf/3s2GmVZBRqmHHw4qX2bnL/8kwBv9S4MybomuDeTdvkxsj3MwFb8+tqypshjg6y9MmApeGZQG9lNCjknE4Vqv6flHzKjd91h/+LkA1ynL6l5SOhJA5PZMdyda0R/AKbroaJTrhivIyfbK98XPucpuCdnFLSjKEBw7CmFDgp97D7cP7qgS36jmJR7yIDmoTFzH6W8Qior1oYCY=~1'
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
                    'appversion': '1.0',
                    'authorization': 'Bearer',
                    'city': "{{cities}}",
                    'content-type': 'application/json',
                    'origin': 'https://www.pvrcinemas.com',
                    'platform': 'WEBSITE',
                    'Cookie': 'ak_bmsc=61718283E0D36E0FC9A999FA36EF067E~000000000000000000000000000000~YAAQF3BWuISDFs2WAQAA3CVI0BvoZsK8fQaiSodyD55+eBsy6wO8CfYl8UeqKTWqVt9o8EI873Lj1PT89kAu4CShIlW6h7N7+2GsgXBGp8hEW/5Ygeey/tTBZgm36j15z0HpwJX1lPj8uoZXgS0Zjy48/63X/Y0X1GSNw6FANjDbap417yiPsKBxSBjwOZnoiHkl55SsXwb/3fXpH54ZJb5IRv03oxSsvQVyQxS4hqAne6J2I1//ziasjDs6dvk//fKbIy2IxfMjpge5Cscm0uuKQfZB6HRZM31/glIqW7vFRA7aTHp6n2FplhKPrf932oND171P/ImPzW73xhOcfxfhA2MUYSXni1k8KIChdMp5h8wV9jUW/Gj23w==; bm_sv=4BE777E05E4608BBDE2053FCD43D607B~YAAQF3BWuCKEFs2WAQAAMTNI0BtlEKi39rdHeACPrG2pOes67eb1I+VJv1JPKYl9bsOs6mK0jZXvcW0l1tEaBGKyB2rbJNqUPvG9+LMrPVmBIHW/s7z1RUVxweozHtcZEvsXbkpsk9LuZNldN26B3wvytm0YdarXM7mJXlqj7GhULBsHU2nBCxwQ5FWQTTgUx+rQnDXJ3p8/JeuICKM0cjpjXRzKqpGJV9imFzlMgFh/8z7SIQvv1EX0gs7fMReYoMdbQgA=~1'
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
