import config
from logging_dir.logging import logger
from miro_boards import boards
from jira import jira_actions
import text


def app_review_started(app):
    # Create review Miro board for new app review
    board_link = board_controller(app)
    inform_customer(app, board_link)


def board_controller(app):
    new_board_id = boards.duplicate_review_board(app)
    try:
        #boards.update_board_items(self.app, new_board_id)
        boards.boardUpdater(app, new_board_id)
    except Exception as err:
        logger.exception(f"Board updates failed, please check logs\n {err}")
    

    new_board_link = f"{config.miro_board_url}{new_board_id}"
    logger.info(f"New board for {app.app_name} can be found at {new_board_link}")
    return new_board_link

def inform_customer(app, board_link):
    logger.info(f"Updating the customer with design review board by commenting to Jira ticket {app.issue_key}")
    jira_actions.comment_to_ticket(app.issue_key, str(text.review_started_message.format(app.app_name, board_link)))
