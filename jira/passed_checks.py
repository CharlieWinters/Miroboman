import config
import text
from jira import jira_actions
from miro_boards import boards
from logging_dir.logging import logger

class welcomeActions(object):

    def __init__(self, app):
        self.app = app
        self.welcome_message = text.welcome_message
        self.controller()

    def controller(self):
        self.add_welcome_message()

    # Post the welcome message with review board to Jira
    def add_welcome_message(self):
        logger.info(f"Commenting welcome message to Jira ticket {self.app.issue_key}")
        jira_actions.comment_to_ticket(self.app.issue_key, str(self.welcome_message.format(self.app.app_name)))




