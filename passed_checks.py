import config
import text
import rest
import jira_actions
import json

class welcomeActions(object):

    def __init__(self, app):
        self.app = app
        self.welcome_message = text.welcome_message
        self.controller()

    def controller(self):
        new_board_link = f"{config.miro_board_url}{self.duplicate_review_board()}"
        print(f"New board for {self.app.app_name} can be found at {new_board_link}")
        self.add_welcome_message(new_board_link)

    # Make a copy of the app review board template for this app review.
    def duplicate_review_board(self):
        print("Duplicating App review board.")
        url = f"{config.miro_base_url}boards?copy_from={config.miro_app_review_template_board}"
        
        payload = {
            "name": f"App review - {self.app.app_name}",
            "policy": {
                "permissionsPolicy": {
                    "collaborationToolsStartAccess": "all_editors",
                    "copyAccess": "anyone",
                    "sharingAccess": "team_members_with_editing_rights"
                },
                "sharingPolicy": {
                    "access": "comment",
                    "inviteToAccountAndBoardLinkAccess": "no_access",
                    "organizationAccess": "edit",
                    "teamAccess": "edit"
                }
            },
            "teamId": f"{config.miro_team_id}",
            "description": f"App review board for {self.app.app_name}"
        }
        try:
            board_dupe_request = rest.put(url, json.dumps(payload), config.miro_auth)
            print(f"Reqeuest status: {board_dupe_request.status_code}")
            board_dupe_request_json = board_dupe_request.json()
        except Exception as err:
            raise err
        board_id = board_dupe_request_json['id']
        return board_id

    # Post the welcome message with review board to Jira
    def add_welcome_message(self, board):
        print(f"Commenting welcome message to Jira ticket {self.app.issue_key}")
        jira_actions.comment_to_ticket(self.app.issue_key, str(self.welcome_message.format(self.app.app_name, board)))




