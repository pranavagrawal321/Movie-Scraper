import argparse
from urllib.parse import urljoin
from curl_cffi import requests
import json
from fake_useragent import UserAgent
from fp.fp import FreeProxy
from time import sleep
import signal
import sys
import re
from random import randint
from config import SITES_LIST

ua = UserAgent()


def create_session(config=None):
    if config is None:
        config = dict()

    session = requests.Session()

    session.impersonate = config.get("IMPERSONATE", "chrome")

    headers = config.get("HEADERS")
    if isinstance(headers, dict):
        session.headers.update(headers)

    proxy = config.get("PROXY")
    if isinstance(proxy, dict):
        session.proxies.update(proxy)

    return session


def process_conditional(data, keys, output):
    if not data:
        return

    if isinstance(keys, str):
        keys = [keys]

    if isinstance(data, list):
        for item in data:
            process_conditional(item, keys, output)

    elif isinstance(data, dict):
        if keys:
            key = keys[0]
            if key in data:
                if key in data:
                    process_conditional(data[key], keys[1:], output)
                else:
                    return
    else:
        if not keys:
            output.add(data)


def process_if_else(data, conditions, output):
    if "IF" in conditions:
        if "VALUE" in conditions['IF']:
            if_keys = conditions['IF']['VALUE'].split(',')
            process_conditional(data, if_keys, output)

    if "ELSE" in conditions:
        if "VALUE" in conditions['ELSE']:
            else_keys = conditions['ELSE']['VALUE'].split(',')
            process_conditional(data, else_keys, output)


def process_json(json_config, data, output, debug=False):
    conditional = None
    key = None

    if "PARENT" in json_config:
        parent_keys = json_config["PARENT"].split(",")

        if isinstance(parent_keys, list) and parent_keys:
            current_key = parent_keys[0]
            remaining_keys = parent_keys[1:]

            if isinstance(data, dict):
                if current_key in data:
                    sub_data = data[current_key]
                    if not sub_data:
                        return

                    if remaining_keys:
                        sub_config = json_config.copy()
                        sub_config["PARENT"] = ",".join(remaining_keys)
                        process_json(sub_config, sub_data, output, debug)
                    else:
                        data = sub_data  # reached target level

                else:
                    return

            elif isinstance(data, list):
                for item in data:
                    sub_config = json_config.copy()
                    sub_config["PARENT"] = ",".join(parent_keys)
                    process_json(sub_config, item, output, debug)
                return  # stop here to avoid extra field-level processing on list container

    if "FIELD_KEYS" in json_config:
        if "VALUE" in json_config["FIELD_KEYS"]:
            if isinstance(json_config["FIELD_KEYS"]["VALUE"], dict):
                conditional = json_config["FIELD_KEYS"]["VALUE"]
            elif isinstance(json_config["FIELD_KEYS"]["VALUE"], str):
                key = json_config["FIELD_KEYS"]["VALUE"]

    if conditional:
        if isinstance(data, list):
            for row in data:
                process_if_else(row, conditional, output)

    if key:
        if isinstance(data, list):
            for row in data:
                process_conditional(row, key, output)


def process_output(data_config, data, output, debug=False):
    if "RULE_JSON" in data_config:
        process_json(data_config['RULE_JSON'], data, output, debug)


def get_all_cities(cities_config, cities, session):
    url = ""
    payload = None
    headers = None
    method = "GET"
    proxies = None

    if "MASTER" in cities_config:
        url = cities_config['MASTER']

    if "PAYLOAD" in cities_config and type(cities_config['PAYLOAD']) == dict:
        payload = json.dumps(cities_config['PAYLOAD'])

    if "HEADERS" in cities_config:
        headers = cities_config['HEADERS']

    if "METHOD" in cities_config:
        method = cities_config['METHOD']

    if "PROXY" in cities_config:
        proxies = cities_config['PROXY']

    response = session.request(
        method=method,
        url=url,
        headers=headers,
        data=payload,
        proxies=proxies,
        timeout=10,
        verify=True
    )

    breakpoint()

    data = response.json()

    process_output(cities_config, data, cities)
    sleep(randint(1, 3))


def get_all_movies(movies_config, movies, cities, session):
    url = ""
    payload = None
    headers = None
    method = "GET"

    if "MASTER" in movies_config:
        url = movies_config['MASTER']

    if "PAYLOAD" in movies_config and isinstance(movies_config['PAYLOAD'], dict):
        payload = movies_config['PAYLOAD']

    if "HEADERS" in movies_config:
        headers = movies_config['HEADERS']

    if "METHOD" in movies_config:
        method = movies_config['METHOD']

    for key, value in payload.items():
        if value.startswith("{{") and value.endswith("}}"):
            if value[2: -2].lower() == 'cities':
                for city in cities:
                    print(f"Processing city {city}")

                    payload['city'] = city
                    headers['city'] = city

                    response = session.request(method, url, headers=headers, data=payload)

                    if response.status_code != 200:
                        continue

                    data = response.json()

                    if "status" in data and data['status'] == 204:
                        continue

                    process_output(movies_config, data, movies)
                    sleep(randint(1, 3))


def get_all_sessions(session_config, movies, cities, session, sessions):
    url = ""
    payload_template = None
    headers_template = None
    method = "GET"

    if "MASTER" in session_config:
        url = session_config['MASTER']

    if "PAYLOAD" in session_config and isinstance(session_config['PAYLOAD'], dict):
        payload_template = session_config['PAYLOAD']

    if "HEADERS" in session_config:
        headers_template = session_config['HEADERS']

    if "METHOD" in session_config:
        method = session_config['METHOD']

    for movie in movies:
        for city in cities:
            print(f"Processing city {city} and movie {movie}")

            payload = json.loads(json.dumps(payload_template))
            headers = headers_template.copy()

            for key, val in payload.items():
                if isinstance(val, str) and val.startswith("{{") and val.endswith("}}"):
                    if val[2:-2] == 'cities':
                        payload[key] = city
                    elif val[2:-2] == 'movie_id':
                        payload[key] = movie

            for key, val in headers.items():
                if isinstance(val, str) and val.startswith("{{") and val.endswith("}}"):
                    if val[2:-2] == 'cities':
                        headers[key] = city

            response = session.request(
                method=method,
                url=url,
                headers=headers,
                data=json.dumps(payload)
            )

            if response.status_code != 200:
                continue

            data = response.json()

            if "status" in data and data['status'] == 204:
                print(data)
                continue

            print("data found")
            breakpoint()

            process_output(session_config, data, sessions, debug=False)
            sleep(randint(1, 3))


def process_child(parent_content, child_content, session):
    cities = set()
    movies = set()
    sessions = set()

    if "cities" in child_content:
        if "PREFIX" in parent_content:
            child_content['cities']['MASTER'] = urljoin(parent_content['PREFIX'], child_content['cities']['MASTER'])

        if "METHOD" in parent_content:
            child_content['cities']['METHOD'] = parent_content['METHOD']

        if "HEADERS" not in child_content['cities']:
            child_content['cities']['HEADERS'] = {}

        if "User-Agent" in parent_content:
            child_content['cities']['HEADERS']['User-Agent'] = parent_content['User-Agent']

        elif "User-Agent" not in parent_content and "User-Agent" not in child_content['cities']['HEADERS']:
            child_content['cities']['HEADERS']['User-Agent'] = ua.random

        if "PROXY" in parent_content and parent_content['PROXY'] == "YES":
            proxy = FreeProxy(country_id=['IN']).get()

            if re.match(r"^http://", proxy):
                proxies = {
                    "http": proxy,
                }
            else:
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
            child_content['cities']['PROXY'] = proxies

        cities_config = child_content["cities"]

        get_all_cities(cities_config, cities, session)

    if "movies" in child_content:
        if "PREFIX" in parent_content:
            child_content['movies']['MASTER'] = urljoin(parent_content['PREFIX'], child_content['movies']['MASTER'])

        if "METHOD" in parent_content:
            child_content['movies']['METHOD'] = parent_content['METHOD']

        if "HEADERS" not in child_content['cities']:
            child_content['movies']['HEADERS'] = {}

        if "User-Agent" in parent_content:
            child_content['movies']['HEADERS']['User-Agent'] = parent_content['User-Agent']

        elif "User-Agent" not in parent_content and "User-Agent" not in child_content['cities']['HEADERS']:
            child_content['movies']['HEADERS']['User-Agent'] = ua.random

        if "PROXY" in parent_content and parent_content['PROXY'] == "YES":
            proxy = FreeProxy(country_id=['IN']).get()

            if re.match(r"^http://", proxy):
                proxies = {
                    "http": proxy,
                }
            else:
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
            child_content['movies']['PROXY'] = proxies

        movies_config = child_content["movies"]

        get_all_movies(movies_config, movies, cities, session)

    if 'sessions' in child_content:
        if "PREFIX" in parent_content:
            child_content['sessions']['MASTER'] = urljoin(parent_content['PREFIX'], child_content['sessions']['MASTER'])

        if "METHOD" in parent_content:
            child_content['sessions']['METHOD'] = parent_content['METHOD']

        if "HEADERS" not in child_content['sessions']:
            child_content['sessions']['HEADERS'] = {}

        if "User-Agent" in parent_content:
            child_content['sessions']['HEADERS']['User-Agent'] = parent_content['User-Agent']
        elif "User-Agent" not in parent_content and "User-Agent" not in child_content['sessions']['HEADERS']:
            child_content['sessions']['HEADERS']['User-Agent'] = ua.random

        if "PROXY" in parent_content and parent_content['PROXY'] == "YES":
            proxy = FreeProxy(country_id=['IN']).get()

            if re.match(r"^http://", proxy):
                proxies = {
                    "http": proxy,
                }
            else:
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
            child_content['sessions']['PROXY'] = proxies

        session_config = child_content["sessions"]

        get_all_sessions(session_config, movies, cities, session, sessions)

    print(sessions)
    breakpoint()


def process_sites(sites_to_be_extracted):
    session = create_session()

    for site in sites_to_be_extracted:
        print(f"Processing {site}")

        parent_content = SITES_LIST[site]
        child_content = SITES_LIST[site]['URL']

        process_child(parent_content, child_content, session)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sites",
        default="*",
        help="Sites to scrape"
    )

    arguments = parser.parse_args(argv)

    if arguments.sites == "*":
        sites_to_be_extracted = SITES_LIST.keys()
    else:
        sites_to_be_extracted = arguments.sites.split(",")

    process_sites(sites_to_be_extracted)


if __name__ == '__main__':
    def sigterm_handler(_signo, _stack_frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)

    args = sys.argv[1:]
    main(args)