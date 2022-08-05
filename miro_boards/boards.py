from typing import Tuple
import config
import rest
import json
from logging_dir.logging import logger

# Make a copy of the app review board template for this app review.
def duplicate_review_board(app):
        logger.info("Duplicating App review board.")
        url = f"{config.miro_base_url}boards?copy_from={config.miro_app_review_template_board}"
        
        payload = {
            "name": f"App review - {app.app_name}",
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
            "description": f"App review board for {app.app_name}"
        }
        
        try:
            board_dupe_request = rest.put(url, json.dumps(payload), config.miro_auth)
            logger.info(f"Reqeuest status: {board_dupe_request.status_code}\n")
            board_dupe_request_json = board_dupe_request.json()
        except Exception as err:
            raise err
        board_id = board_dupe_request_json['id']
        return board_id


class boardUpdater(object):

    def __init__(self, app, board) -> None:
        self.board_id: str = board
        self.app: dict = app
        self.url: str = f"{config.miro_base_url}boards/{board}/"
        self.auth: str = config.miro_auth
        self.controller()
        

    def controller(self) -> None:
        full_board_items = self.get_board_item_data(self.board_id)
        board_app_title_values = self.get_board_title_id(full_board_items)
        url_values = self.get_url_placeholder_ids(full_board_items)
        self.update_app_name(self.app.summary, board_app_title_values)
         # Jira call
        self.add_urls(f"{config.jira_base_url}browse/{self.app.issue_key}", url_values[0])
        # install url call
        self.add_urls(self.app.installation_url, url_values[1])

    # Get the full list of items on the board
    def get_board_item_data(self, board: str) -> list:
        logger.info(f"Getting board items for board with id {board}\n")
        url = f"{self.url}items?limit=50"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"{self.auth}"
        }
        response = rest.get(url, headers=headers)
        logger.info(f"Board item call: {response.status_code}\n")
        board_items = response.json()['data']
        while 'next' in response.json()['links']:
            logger.info("'next' value found. Calling again")
            new_url = response.json()['links']['next']
            response = rest.get(new_url, headers=headers)
            board_items.extend(response.json()['data'])
        return board_items

    # Retrieve id for board title
    def get_board_title_id(self, board_items: list) -> Tuple[str, dict]:
        logger.info(f"Getting board app title id\n")
        for board_item in board_items:
            if "text" in board_item['type'] and '_' not in board_item['type']:
                logger.info(f"Text item found\n")
                if "app-name" in board_item['data']['content']:
                    board_id = board_item['id']
                    board_id_position = board_item['position']
                    logger.info(f"Found title: {board_item['data']['content']} | Id: {board_id}\n")
                    return [board_id, board_id_position]

    # Get the ids and position for the url fields (jira ticket and install url)
    def get_url_placeholder_ids(self, board_items):
        logger.info("Retrieving url board values\n")
        url_placeholders = []
        for board_item in board_items:
            if "shape" in board_item['type']:
                logger.info("Shape found!\n")
                if "jira_url" in board_item['data']['content']:
                    jira_url_data = {'id': board_item['id'], 'position': board_item['position']}
                    url_placeholders.append(jira_url_data)
                if "install_url" in board_item['data']['content']:
                    install_url_data = {'id': board_item['id'], 'position': board_item['position']}
                    url_placeholders.append(install_url_data)
        logger.info(f"URL Placeholder values: {url_placeholders}\n")
        return url_placeholders

    # Update the value of the app title on the board
    def update_app_name(self, app_name, board_app_title_values) -> None:
        logger.info(f"Updating app name on board.\n")
        board_app_title_id = board_app_title_values[0]
        board_app_title_position = board_app_title_values[1]
        # remove unwanted values from position object
        board_app_title_position = self.position_obj_trimmer(board_app_title_position)
        url = f"{self.url}/texts/{board_app_title_id}"
        payload = json.dumps({
                "data": {"content": f"{app_name}"},
                "style": {
                    "color": "#1a1a1a",
                    "fillOpacity": "1.0",
                    "fontFamily": "open_sans",
                    "fontSize": "288",
                    "textAlign": "left"
                },
                "position": board_app_title_position
                })
        self.send_update_request(url, payload)

    # Update the url fields (jira ticket and install url)
    def add_urls(self, content_url: str, url_values: dict) -> None:
        logger.info(f"Updating urls on board.\n")
        id = url_values['id']
        position = url_values['position']
        position = self.position_obj_trimmer(position)
        url = f"{self.url}shapes/{id}"
        payload = json.dumps({
                        "data": {
                            "content": f"{content_url}",
                            "shape": "rectangle"
                        },
                        "style": {
                            "borderColor": "#1a1a1a",
                            "borderOpacity": "1.0",
                            "borderStyle": "normal",
                            "borderWidth": "2.0",
                            "color": "#1a1a1a",
                            "fillOpacity": "1.0",
                            "fontFamily": "open_sans",
                            "fontSize": "31",
                            "textAlign": "center",
                            "textAlignVertical": "middle"
                        },
                        "position": position
                    })
        self.send_update_request(url, payload)

    # Function to remove 'origin' and 'relevantTo' values from position object  
    def position_obj_trimmer(self, position: dict) -> dict:
        rem_list = ['origin', 'relativeTo']
        position = dict([(key, val) for key, val in position.items() if key not in rem_list])
        return position

    # Send the update request
    def send_update_request(self, url: str, payload: dict):
        response = rest.patch(url, payload, self.auth)
        if response.status_code in range(200, 210):
            logger.info(f"Updated board with ID {self.board_id}\n")
        else:
            logger.info(f"Update failed for board with ID {self.board_id}\n")