"""
Module to extract the developer responses from the Marketplace listing typeform

Response body is made up of questions and responses. 

We first extract the questions and their ID and create a list of dicts.

We then use the question ID to match with the answer id and add the answers to the existing corresponding question dict in the original list of dicts we made. 


"""
from logging_dir.logging import logger


class FromDataExtractor():

    def __init__(self, webhook) -> None:
        self.raw_form_data = webhook
        self.typeform_obj = {"fields": []}

    def controller(self):
        logger.info("Extracting typeform data")
        self.capture_questions()
        self.capture_responses() 
        return self.typeform_obj
        

    def capture_questions(self):
        for i in self.raw_form_data['form_response']['definition']['fields']:
            field_data = {'id' : i['id'], 'title' : i['title']}
            self.typeform_obj['fields'].append(field_data)

    def capture_responses(self):
        for key in self.raw_form_data['form_response']['answers']:
            for entry in self.typeform_obj['fields']:
                if key['field']['id'] == entry['id']:
                    #print(f"Match! - {key['field']['id']} and {entry['id']} for {entry['title']}")
                    if 'text' in key['type']:
                        new_vals = {'type': key['type'], 'response': key['text']}
                        entry.update(new_vals)
                    elif 'file_url' in key['type']:
                        new_vals = {'type': key['type'], 'response': key['file_url']}
                        entry.update(new_vals)
                    elif 'choices' in key['type']:
                        new_vals = {'type': key['type'], 'response': key['choices']}
                        entry.update(new_vals)
                    else:
                        entry['response'] = None 
