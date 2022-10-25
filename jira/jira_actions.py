from shared import rest
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


# Find Jira ticket by App ID
def find_jira_by_appid(app_id):
    logger.info(f"Searching for existing issues with appId {app_id}")
    url = f"{config.jira_base_url}rest/api/3/search"
    payload = json.dumps({
        "jql": f"project = art and 'App Id[Short text]' ~ '{app_id}'"
    })
    results = rest.post(url, payload, config.jira_auth)
    results_json = results.json()
    if results_json['total'] == 1:
        jira_key = results_json['issues'][0]['key']
        logger.info(f"Matching ticket found: {jira_key}")
        return jira_key
    elif results_json['total'] > 1:
        logger.info(f"Multiple issues found, exiting - logic still to be written.")
        return False
    else:
        logger.info(f"No matching Jira ticket found for app '{app_id}'")
        return False

# Create subtask for typeform assets
def create_subtask(jira_key, app_name):
    url = f"{config.jira_base_url}rest/api/2/issue"
    payload = json.dumps({
        "fields": {
            "project": {
            "key": f"{config.jira_project_key}"
            },
            "summary": f"Marketing assets for {app_name}",
            "parent": {
            "key": f"{jira_key}"
            },
            "description": f"This is a subtask to {jira_key} for reviewing app listing assets",
            "issuetype": {
            "id": "10003"
            }
        }
    })
    results = rest.post(url, payload, config.jira_auth)
    results_json = results.json()
    subtask_key = results_json['key']
    logger.info(f"Subtask with key '{subtask_key} created.")
    return subtask_key

# Add images to jira ticket
def add_images_to_jira(issue_key, file):
    payload = None
    url = f"{config.jira_base_url}/rest/api/2/issue/{issue_key}/attachments"
    # File format passed needs to be ('file', (f"{file}", open(f"{path}/{file}",'rb'), 'image/jpeg')) ]
    custom_header = ['X-Atlassian-Token', 'no-check']
    rest.post(url, payload, config.jira_auth, custom_header, file)

