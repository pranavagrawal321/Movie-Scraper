import argparse
from urllib.parse import urljoin
import requests
import json
from config import SITES_LIST


def process_conditional(data, keys, output):
    if isinstance(data, list):
        for item in data:
            process_conditional(item, keys, output)
    elif isinstance(data, dict):
        if keys:
            key = keys[0]
            if key in data:
                process_conditional(data[key], keys[1:], output)
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


def process_json(json_config, data, output):
    conditional = {}

    if "PARENT" in json_config:
        parent_keys = json_config['PARENT'].split(",")

        for parent_key in parent_keys:
            data = data[parent_key]

    if "FIELD_KEYS" in json_config:
        if "VALUE" in json_config['FIELD_KEYS']:
            if isinstance(json_config['FIELD_KEYS']['VALUE'], dict):
                conditional = json_config['FIELD_KEYS']['VALUE']

    if conditional:
        if isinstance(conditional, dict):
            process_if_else(data, conditional, output)


def process_output(cities_config, data, output):
    if "RULE_JSON" in cities_config:
        process_json(cities_config['RULE_JSON'], data, output)

def get_all_cities(cities_config, cities):
    url = ""
    payload = None
    headers = None
    method = "GET"

    if "MASTER" in cities_config:
        url = cities_config['MASTER']

    if "PAYLOAD" in cities_config and type(cities_config['PAYLOAD']) == dict:
        payload = json.dumps(cities_config['PAYLOAD'])

    if "HEADERS" in cities_config:
        headers = cities_config['HEADERS']

    if "METHOD" in cities_config:
        method = cities_config['METHOD']

    response = requests.request(method, url, headers=headers, data=payload)
    data = response.json()

    process_output(cities_config, data, cities)


def process_child(parent_content, child_content):
    cities = set()

    if "cities" in child_content:
        if "PREFIX" in parent_content:
            child_content['cities']['MASTER'] = urljoin(parent_content['PREFIX'], child_content['cities']['MASTER'])

        if "METHOD" in parent_content:
            child_content['cities']['METHOD'] = parent_content['METHOD']

        cities_config = child_content["cities"]

        get_all_cities(cities_config, cities)

    print(cities)

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