import rest
from data_definer import dataSummary
import jira_actions

def url_check(app):
    url = app.project_link
    url_call = rest.get(url)
    if url_call.status_code != range(200, 2001):
        comment = f"Invalid response for {url}, Response was: {url_call.status_code}"
        print(comment)
        jira_actions.comment_to_ticket(app.issue_key, comment, True)
        return False
    else:
        print(f"Successful call for {url}, Response was {url_call.status_code}")
        return True



