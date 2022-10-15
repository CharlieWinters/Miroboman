from logging_dir.logging import logger
import config

class typeformDataSummary():
    def __init__(self, request_data):
        try:
            self.app_name = [i['response'] for i in request_data['fields'] if config.typeform_app_name in i['id']]
            self.app_id = [i['response'] for i in request_data['fields'] if config.typeform_app_id in i['id']]
            self.dev_name = [i['response'] for i in request_data['fields'] if config.typeform_dev_name in i['id']]
            self.dev_email = [i['response'] for i in request_data['fields'] if config.typeform_dev_email in i['id']]
            self.short_desc = [i['response'] for i in request_data['fields'] if config.typeform_short_desc in i['id']]
            self.full_desc = [i['response'] for i in request_data['fields'] if config.typeform_full_desc in i['id']]
            self.tos = [i['response'] for i in request_data['fields'] if config.typeform_tos in i['id']]
            self.privacy_policy = [i['response'] for i in request_data['fields'] if config.typeform_privacy_policy in i['id']]
            self.helpfull_links = [i['response'] for i in request_data['fields'] if config.typeform_helpfull_links in i['id']]
            self.full_condensed_typeform = request_data
        except Exception as err:
            logger.exception(err)