import rest
import config
from data_definer import dataSummary
import json

# Comment to the Jira ticket
def comment_to_ticket(issue_key, comment, public=True):
    print(f"Commenting to {issue_key}")
    url = f"{config.jira_base_url}rest/api/2/issue/{issue_key}/comment"

    if public is True:
        payload = json.dumps({"body": comment })
    else:
        payload = json.dumps({ "visibility": {"type": "role", "value": "Service Desk Team"}, 
                            "body": comment })

    try:
        post_comment = rest.post(url, payload, config.jira_auth)
        print(f"Comment status: {post_comment.status_code}")
        #print(f"Failure: {post_comment.content}")
    except Exception as err:
        raise err
