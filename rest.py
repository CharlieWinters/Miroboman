from urllib import response
from urllib.error import HTTPError
import requests

def get(url, headers=""):
    print(f"Making a GET to {url}")
    try:
        response_data = requests.get(url, headers=headers)
    except HTTPError as err:
        raise err
    status_check(response_data)
    return response_data

def post(url, payload, auth):
    print(f"Making a Post to {url}")
    headers = {'Authorization': f'{auth}',
                'Content-Type': 'application/json'}
    try:
        response_data = requests.post(url, data=payload, headers=headers)
    except HTTPError as err:
        raise err
    status_check(response_data)
    return response_data

def put(url, payload, auth):
    print(f"Making a PUT to {url}")
    headers = {'Authorization': f'{auth}',
                'Content-Type': 'application/json'}
    try:
        response_data = requests.put(url, data=payload, headers=headers)
    except HTTPError as err:
        raise err
    status_check(response_data)    
    return response_data

# Check the status of the request, if 4XX or 5XX then print error details. 
def status_check(status):
    if status.status_code in range(300, 600):
        print(f"There was an issue with the call, status_code is {status.status_code}\n")
        print(f"Error details are: {status.content}")
        print(f"Call details are: {status.headers}")