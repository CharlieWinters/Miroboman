from urllib import response
from urllib.error import HTTPError
import requests
from logging_dir.logging import logger

# GET
def get(url, headers=None):
    logger.info(f"Making a GET to {url}\n")
    try:
        response_data = requests.get(url, headers=headers)
    except HTTPError as err:
        logger.exception(err)
    status_check(response_data)
    return response_data

# POST
def post(url, payload, auth, custom_header=None, file=None):
    logger.info(f"Making a Post to {url}")
    headers = {'Authorization': f'{auth}',
                'Content-Type': 'application/json'}
    if custom_header != None:
        # POST with custom header and pass files to be added
        headers = {'Authorization': f'{auth}',
                f'{custom_header[0]}': f'{custom_header[1]}'}
        try:
            response_data = requests.post(url, data=payload, headers=headers, files=file)
        except HTTPError as err:
            logger.exception(err)
    else:
        # Normal Post
        try:
            response_data = requests.post(url, data=payload, headers=headers)
        except HTTPError as err:
            logger.exception(err)
    status_check(response_data)
    return response_data

# PUT
def put(url, payload, auth):
    logger.info(f"Making a PUT to {url}")
    headers = {'Authorization': f'{auth}',
                'Content-Type': 'application/json'}
    try:
        response_data = requests.put(url, data=payload, headers=headers)
    except HTTPError as err:
        logger.exception(err)
    status_check(response_data)    
    return response_data

# PATCH
def patch(url, payload, auth):
    logger.info(f"Making a Post to {url}")
    headers = {'Authorization': f'{auth}',
                'Content-Type': 'application/json'}
    try:
        response_data = requests.patch(url, data=payload, headers=headers)
    except HTTPError as err:
        logger.exception(err)
    status_check(response_data)
    return response_data

# Check the status of the request, if 4XX or 5XX then print error details. 
def status_check(status):
    if status.status_code in range(300, 600):
        logger.info(f"There was an issue with the call, status_code is {status.status_code}\n")
        logger.info(f"Error details are: {status.content}")
        logger.info(f"Call details are: {status.headers}")