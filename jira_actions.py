import rest
import config
import json
from logging_dir.logging import logger

# Comment to the Jira ticket
def comment_to_ticket(issue_key, comment, public=True):
    logger.info(f"Commenting to {issue_key}")
    url = f"{config.jira_base_url}rest/api/2/issue/{issue_key}/comment"

    if public is True:
        payload = json.dumps({"body": comment })
    else:
        payload = json.dumps({ "visibility": {"type": "role", "value": "Service Desk Team"}, 
                            "body": comment })

    try:
        post_comment = rest.post(url, payload, config.jira_auth)
        logger.info(f"Comment status: {post_comment.status_code}")
    except Exception as err:
        logger.exception(err)
