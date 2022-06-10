from urllib import response
from urllib.error import HTTPError
import requests
import config

def get(url):
    print(f"Making a GET to {url}")
    try:
        response_data = requests.get(url)
    except HTTPError as err:
        raise err
    return response_data

def post(url, payload):
    print(f"Making a Post to {url}")
    headers = {'Authorization': f'{config.jira_auth}',
                'Content-Type': 'application/json'}
    try:
        response_data = requests.post(url, data=payload, headers=headers)
    except HTTPError as err:
        raise err
    return response_data