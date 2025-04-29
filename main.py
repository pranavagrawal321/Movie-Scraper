import argparse
from urllib.parse import urljoin
import requests
import json
from config import SITES_LIST


def process_json(json_config, data):
    if "PARENT" in json_config:
        parent_keys = json_config['PARENT'].split(",")

        for parent_key in parent_keys:
            data = data[parent_key]

    print(json_config)

    # if isinstance(data, list):
    #     for item in data:
    #


def process_output(cities_config, data):
    if "RULE_JSON" in cities_config:
        process_json(cities_config['RULE_JSON'], data)

def get_all_cities(cities_config):
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

    process_output(cities_config, data)




def process_child(parent_content, child_content):
    if "cities" in child_content:
        if "PREFIX" in parent_content:
            child_content['cities']['MASTER'] = urljoin(parent_content['PREFIX'], child_content['cities']['MASTER'])

        if "METHOD" in parent_content:
            child_content['cities']['METHOD'] = parent_content['METHOD']

        cities_config = child_content["cities"]

        cities = get_all_cities(cities_config)


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