from requests import request
import config
import rest
import json

# Make a copy of the app review board template for this app review.
def duplicate_review_board(app):
        print("Duplicating App review board.")
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
            #board_dupe_request = rest.post(url, payload, config.miro_auth)
            print(f"Reqeuest status: {board_dupe_request.status_code}")
            board_dupe_request_json = board_dupe_request.json()
        except Exception as err:
            raise err
        board_id = board_dupe_request_json['id']
        return board_id

### BUILD A FUNCTION TO UPDATE THE MIRO BOARD WITH THE APP NAME, JIRA TICKET NUMEBR, AND INSTALL URL.
def update_board_items(app, board):
    full_board_items = get_board_item_data(board)
    board_app_title_values = get_board_title(full_board_items)
    update_item(app.app_name, board, board_app_title_values)





def get_board_item_data(board):
    print(f"Getting board items for board iwth id {board}")
    url = f"{config.miro_base_url}boards/{board}/items?limit=50"
    headers = config.miro_auth
    response = rest.get(url, headers=headers)
    board_items = response.json()['data']
    while 'next' in response.json()['links']:
        new_url = response.json()['links']['next']
        response = rest.get(new_url, config.miro_auth)
        board_items.extend(response.json()['data'])
    return board_items


def get_board_title(board_items):
    for board_item in board_items['data']:
        if "text" in board_item['type'] and '_' not in board_item['type']:
            if "app-name" in board_item['data']['content']:
                board_id = board_item['id']
                board_id_position = board_item['position']
                print(f"Found title: {board_item['data']['content']}\nId: {board_id}")
                return [board_id, board_id_position]

# Update the value of the app title on the board
def update_item(app_name, board, board_app_title_values):
    board_app_title_id = board_app_title_values[0]
    board_app_title_position = board_app_title_values[1]
    url = f"{config.miro_base_url}boards/{board}/texts/{board_app_title_id}"
    payload = {
            "data": {
                "content": f"{app_name}",
                "style": {
                    "color": "#1a1a1a",
                    "fillOpacity": "1.0",
                    "fontFamily": "open_sans",
                    "fontSize": "288",
                    "textAlign": "left"
                },
                "position": board_app_title_position 
                }
            }
####FINSISH BUILDING UPDATE REQUEST TO ####