import os
from logging_dir.logging import logger

## Jira ##       

jira_auth = os.environ["JIRA_AUTH"]
jira_base_url = os.environ["JIRA_BASE_URL"]
jira_project_key = os.environ["JIRA_PROJECT_KEY"]
jira_subtask_id = os.environ["JIRA_SUBTASK_ID"]

## Miro ##

miro_auth = os.environ["MIRO_AUTH"]
miro_base_url = "https://api.miro.com/v2/"
miro_board_url = "https://miro.com/app/board/"
miro_app_review_proj_id = "3458764528159331663"
miro_app_review_template_board = "uXjVOmfWmQU="
miro_account_id = "3074457345710752794"
miro_team_id = "3074457345710752794"


## Typeform ##

# Form Question IDs (IDs for each question on the form)

if os.environ["ENVIRONMENT"] == 'LOCAL':
    print("Miroboman is being run locally.")
    env = "DEV"
    typeform_app_name = 'Aepp7sDitPj0'
    typeform_app_id = 'ZiZlqPZXDBHn'
    typeform_dev_name = '10SaXHTpUvHh'
    typeform_dev_email = 'MocvRFSxsbZs'
    typeform_short_desc = 'YbGLpg35xA2k'
    typeform_full_desc = 'Uf9t5hNr6Fh8'
    typeform_tos = 'frvdQgt3bZQo'
    typeform_privacy_policy = 'vVM9ddt5l9Yz'
    typeform_helpfull_links = '7eYXYqCksaQg'
    typeform_key_features = '5NIGXg83ILog'
    typeform_connect_how = 'iFwhQv2SF3ze'
    typeform_categories = 'UdFjjrTkTkYj'
    typeform_tags = 'UsXsUBfDyQzM'
else:
    env = "PROD"
    typeform_app_name = 'gxJcINDmMzWc'
    typeform_app_id = 'j3olmO5Sl7Ax'
    typeform_dev_name = 'AhjQFofHGzwR'
    typeform_dev_email = 'b97C9pVZgSzp'
    typeform_short_desc = 'ZJ9hXw2xRUAj'
    typeform_full_desc = '2x8EJfWgq3iE'
    typeform_tos = 'FaQA5YgAK2y5'
    typeform_privacy_policy = '1uSGj4dUq69O'
    typeform_helpfull_links = 'qYwAcY0nW3fq'
    typeform_key_features = 'PaVNbXNqcCxk'
    typeform_connect_how = 'xYplFTjflDUE'
    typeform_categories = 'iwVLn5XRrXQR'
    typeform_tags = 'YIMrLuGsvmP8'