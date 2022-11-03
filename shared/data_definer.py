from logging_dir.logging import logger

class dataSummary():
    def __init__(self, request_data):
        try:
            self.issue_key = request_data.issue_key
            self.app_name = request_data.app_name
            self.summary = request_data.summary
            self.description = request_data.description
            self.user_id = request_data.user_id
            self.app_id = request_data.app_id
            self.setup_instructions = request_data.setup_instructions
            self.scopes = request_data.scopes
            self.installation_url = request_data.installation_url
            self.recording_link = request_data.recording_link
            self.installation_credentials = request_data.integration_credentials
        except Exception as err:
            logger.exception(err)
    