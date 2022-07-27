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
            print(f"Reqeuest status: {board_dupe_request.status_code}")
            board_dupe_request_json = board_dupe_request.json()
        except Exception as err:
            raise err
        board_id = board_dupe_request_json['id']
        return board_id

### BUILD A FUNCTION TO UPDATE THE MIRO BOARD WITH THE APP NAME, JIRA TICKET NUMEBR, AND INSTALL URL.
def update_board_items(app, board):
    full_board_items = get_board_item_data(board)
    board_app_title_values = get_board_title_id(full_board_items)
    url_values = get_url_placeholder_ids(full_board_items)
    update_app_name(app.summary, board, board_app_title_values)
    # Jira call
    url_payload_builder(board, f"{config.jira_base_url}browse/{app.issue_key}", url_values[0])
    # install url call
    url_payload_builder(board, app.installation_url, url_values[1])


def get_board_item_data(board):
    print(f"Getting board items for board with id {board}\n")
    url = f"{config.miro_base_url}boards/{board}/items?limit=50"
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"{config.miro_auth}"
}
    response = rest.get(url, headers=headers)
    print(f"Board item call: {response.status_code}")
    board_items = response.json()['data']
    while 'next' in response.json()['links']:
        print("'next' value found. Calling gain")
        new_url = response.json()['links']['next']
        response = rest.get(new_url, headers=headers)
        board_items.extend(response.json()['data'])
    return board_items

# Retrieve id for board title
def get_board_title_id(board_items):
    print(f"Getting board app title id")
    for board_item in board_items:
        if "text" in board_item['type'] and '_' not in board_item['type']:
            print(f"Text item found\n")
            if "app-name" in board_item['data']['content']:
                board_id = board_item['id']
                board_id_position = board_item['position']
                print(f"Found title: {board_item['data']['content']} | Id: {board_id}\n")
                return [board_id, board_id_position]

# Get the ids and position for the url fields (jira ticket and install url)
def get_url_placeholder_ids(board_items):
    print("Retrieving url board values\n")
    url_placeholders = []
    for board_item in board_items:
        if "shape" in board_item['type']:
            print("Shape found!\n")
            if "jira_url" in board_item['data']['content']:
                jira_url_data = {'id': board_item['id'], 'position': board_item['position']}
                url_placeholders.append(jira_url_data)
            if "install_url" in board_item['data']['content']:
                install_url_data = {'id': board_item['id'], 'position': board_item['position']}
                url_placeholders.append(install_url_data)
    print(f"URL Placeholder values: {url_placeholders}\n")
    return url_placeholders

# Update the value of the app title on the board
def update_app_name(app_name, board, board_app_title_values):
    print(f"Updating app name on board.")
    board_app_title_id = board_app_title_values[0]
    board_app_title_position = board_app_title_values[1]
    # remove unwanted values from position object
    board_app_title_position = position_obj_trimmer(board_app_title_position)
    url = f"{config.miro_base_url}boards/{board}/texts/{board_app_title_id}"
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
    response = rest.patch(url, payload, config.miro_auth)
    if response.status_code in range(200, 210):
        print(f"Updated app name on board {board}")
    else:
        print("Update failed")

# Update the url fields (jira ticket and install url)
def url_payload_builder(board, app, url_values):
    print(f"Updating urls on board.")
    print(url_values)
    id = url_values['id']
    position = url_values['position']
    position = position_obj_trimmer(position)
    url = f"{config.miro_base_url}boards/{board}/shapes/{id}"
    payload = json.dumps({
                    "data": {
                        "content": f"{app}",
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
    print(payload)
    send_update_request(url, payload)

# Send the update request
def send_update_request(url, payload):
    response = rest.patch(url, payload, config.miro_auth)

# function to remove 'origin' and 'relevantTo' values from position object  
def position_obj_trimmer(position):
    rem_list = ['origin', 'relativeTo']
    position = dict([(key, val) for key, val in position.items() if key not in rem_list])
    return position