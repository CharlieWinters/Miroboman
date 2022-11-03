import shared.rest as rest
from shared.data_definer import dataSummary
from logging_dir.logging import logger

def url_check(url):
    url_call = rest.get(url)
    if url_call.status_code in range(200, 202):
        logger.info(f"Successful call for {url}, Response was {url_call.status_code}")
        return [True]
    else:
        logger.info(f"Invalid response for {url}, Response was: {url_call.status_code}")
        return [False, url_call.status_code]

