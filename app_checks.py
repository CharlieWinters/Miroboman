import rest
from data_definer import dataSummary
import jira_actions

def url_check(url):
    url_call = rest.get(url)
    if url_call.status_code in range(200, 202):
        print(f"Successful call for {url}, Response was {url_call.status_code}")
        return [True]
    else:
        print(f"Invalid response for {url}, Response was: {url_call.status_code}")
        return [False, url_call.status_code]

