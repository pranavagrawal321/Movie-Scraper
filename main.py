import argparse
from urllib.parse import urljoin
from curl_cffi import requests
import json
from fake_useragent import UserAgent
from fp.fp import FreeProxy
from config import SITES_LIST

ua = UserAgent()


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


def process_if_else(data, conditions, output, test):
    if "IF" in conditions:
        if "VALUE" in conditions['IF']:
            if_keys = conditions['IF']['VALUE'].split(',')
            process_conditional(data, if_keys, output)

    if "ELSE" in conditions:
        if "VALUE" in conditions['ELSE']:
            else_keys = conditions['ELSE']['VALUE'].split(',')
            process_conditional(data, else_keys, output)


def process_json(json_config, data, output, test):
    conditional = None
    key = None

    if "PARENT" in json_config:
        parent_keys = json_config['PARENT'].split(',')

        for key in parent_keys:
            if isinstance(data, dict):
                if key in data:
                    data = data[key]

                    if not data:
                        return

                else:
                    return

    if "FIELD_KEYS" in json_config:
        if "VALUE" in json_config["FIELD_KEYS"]:
            if isinstance(json_config['FIELD_KEYS']['VALUE'], dict):
                conditional = json_config['FIELD_KEYS']['VALUE']

            elif isinstance(json_config['FIELD_KEYS']['VALUE'], str):
                key = json_config['FIELD_KEYS']['VALUE']

    if conditional:
        if isinstance(data, list):
            for row in data:
                process_if_else(row, conditional, output, test)

    if key:
        if isinstance(data, list):
            for row in data:
                process_conditional(row, key, output)


def process_output(cities_config, data, output, test):
    if "RULE_JSON" in cities_config:
        process_json(cities_config['RULE_JSON'], data, output, test)


def get_all_cities(cities_config, cities):
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

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        data=payload,
        proxies=proxies,
        timeout=10,
        verify=True
    )

    data = response.json()

    process_output(cities_config, data, cities, test=False)


def get_all_movies(movies_config, movies, cities, test=False):
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

                    response = requests.request(method, url, headers=headers, data=payload)

                    if response.status_code != 200:
                        continue

                    data = response.json()

                    if "status" in data and data['status'] == 204:
                        continue

                    process_output(movies_config, data, movies, test)


def process_child(parent_content, child_content):
    cities = set()
    movies = set()

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
            proxy = FreeProxy().get()

            proxies = {
                "http": proxy,
            }

            child_content['cities']['PROXY'] = proxies

        cities_config = child_content["cities"]

        get_all_cities(cities_config, cities)

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
            proxy = FreeProxy().get()

            proxies = {
                "http": proxy,
            }

            child_content['movies']['PROXY'] = proxies

        movies_config = child_content["movies"]

        get_all_movies(movies_config, movies, cities, test=True)


def process_sites(sites_to_be_extracted):
    for site in sites_to_be_extracted:
        print(f"Processing {site}")

        parent_content = SITES_LIST[site]
        child_content = SITES_LIST[site]['URL']

        process_child(parent_content, child_content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sites",
        default="*",
        help="Sites to scrape"
    )

    args = parser.parse_args()

    if args.sites == "*":
        sites_to_be_extracted = SITES_LIST.keys()
    else:
        sites_to_be_extracted = args.sites.split(",")

    process_sites(sites_to_be_extracted)


if __name__ == '__main__':
    main()