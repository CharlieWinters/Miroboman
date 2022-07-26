import config
import text
import rest
import jira_actions
import json
from miro_boards import boards

class welcomeActions(object):

    def __init__(self, app):
        self.app = app
        self.welcome_message = text.welcome_message
        self.controller()

    def controller(self):
        new_board_id = boards.duplicate_review_board(self.app)
        try:
            boards.update_board_items(self.app, new_board_id)
        except:
            print("Board updates failed, please check logs")
        

        new_board_link = f"{config.miro_board_url}{new_board_id}"
        print(f"New board for {self.app.app_name} can be found at {new_board_link}")
        self.add_welcome_message(new_board_link)

    # Post the welcome message with review board to Jira
    def add_welcome_message(self, board):
        print(f"Commenting welcome message to Jira ticket {self.app.issue_key}")
        jira_actions.comment_to_ticket(self.app.issue_key, str(self.welcome_message.format(self.app.app_name, board)))




