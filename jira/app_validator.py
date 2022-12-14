from jira import app_checks, jira_actions
import text
from logging_dir.logging import logger


class appComponentCheck(object):

    def __init__(self, app) -> None:
        self.app = app
        # Any Dict entry that will contain a URL must have a key that ends in '_url'
        self.review_items = {
                            "setup_instructions_url": [app.setup_instructions, False],
                            "scopes": [app.scopes, False],
                            "installation_url": [app.installation_url, False],
                            "recording_url": [app.recording_link, False],
                            "installation_credentials": [app.installation_credentials, False]
                            }
        
        #self.controller()

    def controller(self):
        # removed description due to https://github.com/CharlieWinters/Miroboman/issues/3
        # self.description_check()
        self.scopes_check()
        self.integration_creds_check()
        for key, value in self.review_items.items():
            
            if self.is_it_url(key):
                self.url_checks(key, value)
            else:
                logger.info(f"No URL check needed for {key}")
        # Check if any failures have been recorded
        if self.pass_check():
            return True
        
    ''' 
    # removed description due to https://github.com/CharlieWinters/Miroboman/issues/3
    # Once fixed the entry in self.review_items will need to be added back i.e. '"description": [app.description, False],'
    def description_check(self):
        logger.info(f"\nChecking Description link.\n")
        # Nothing to check yet
        self.review_items['description'][1] = True
    '''

    def scopes_check(self):
        logger.info(f"\nChecking Scopes.\n")
        # Nothing to check yet
        self.review_items['scopes'][1] = True

    def integration_creds_check(self):
        logger.info(f"\nChecking Integration instructions.\n")
        # Nothing to check yet
        self.review_items['installation_credentials'][1] = True

    def url_checks(self, key, val):
        logger.info(f"\nChecking {key} link.\n")
        app_check_result = app_checks.url_check(val[0])
        if app_check_result[0]:
            logger.info("True - URL test passed.")
            self.review_items[key][1] = True
        else:
            self.review_items[key].append(app_check_result[1])
            logger.info("False - URL test failed")

    def pass_check(self):
        # Check for False values and comment failures to Jira ticket
        failures = []
        for key, value in self.review_items.items():
            if not value[1]:
                if self.is_it_url(key):
                    message = f"The URL check failed for {key}. URL: {value[0]} Response: {value[2]}"
                    failures.append(message)
                else:
                    message = f"Problem encountered with value(s) provided for {key}. Details to follow."
                    failures.append(message)
        # Comment the failures to the Jira ticket and reject ticket.
        if failures:
            logger.info(f"Rejecting app as {len(failures)} failures found.")
            jira_actions.comment_to_ticket(self.app.issue_key, text.failure_message.format("\n".join(map(str,failures))), False)
            return False
        else:
            logger.info(f"{len(failures)} failures found. Proceeding with greeting message.")
            return True

    # Check if review item has 'url' in name, if True expect URL value 
    def is_it_url(self, key):
        if key.find("_url") !=-1:
            return True
