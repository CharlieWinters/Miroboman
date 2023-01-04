from logging_dir.logging import logger
from typeform import typeform_processing, typeform_data_points, image_manager
from jira import jira_actions
import os


def boss(webhook):
    logger.info(f"Beginning Typeform processing....")
    # Parse the raw typeform response and create condensed block
    typeform_data_obj = typeform_processing.FromDataExtractor(webhook)
    typeform_data = typeform_data_obj.controller()
    # Create typeform data block - this is all we'll need from here on out
    typeform_app = typeform_data_points.typeformDataSummary(typeform_data)
    jira_key = jira_actions.find_jira_by_appid(typeform_app.app_id[0])
    # Check if jira ticket is found with matching ID
    if not jira_key:
        logger.info("Abandoning typeform autoamtion, no Jira ticket found.")
        return
    
    try:
        if not image_manager.image_consultant(typeform_app):
            return
    except Exception as err:
        raise err

    
    # Create subtask
    subtask = jira_actions.create_subtask(jira_key, typeform_app)
    # The name of the directory for where the app's images are stored - this is a dupe of imagemanager.folder_creator - this will need refactoring
    dir_name = (typeform_app.app_name[0].lower()).replace(" ", "_")
    # Get the list of files in the directory with modified app name
    files = image_manager.file_grabber(dir_name)
    # Build the full path to where the images are stored. 
    path = f"{os.getcwd()}/typeform/temp/{dir_name}/"
    # Add images to subtask
    jira_actions.add_images_to_jira(subtask, image_manager.file_list_creator(files, path))
    # Retrieve jira issue description and create the updated one
    updated_description = description_builder(jira_actions.get_jira_issue_details(subtask, "description,attachment"))
    # Update description on ticket
    jira_actions.update_field(subtask, updated_description)
    # Remove the image files from the server
    image_manager.clean_up(path)

# Add attachments to description
def description_builder(ticket_details):
    description = ticket_details['fields']['description']
    attachments = ticket_details['fields']['attachment']
    # Place holder str vairable
    attachment_block = "\n"
    # Build the Markdown table for provided images, format is as below.
    """ |Logo| !logo.jpeg|thumbnail! |
        |Visual 1| !visual_1.png|thumbnail! | """
    for image in attachments:
        temp_string = f"|{image['filename'].split('.')[0].replace('_', ' ')}|!{image['filename']}|thumbnail!|\n"
        attachment_block += temp_string
    # Append the Markdown table to the original description
    new_description = description + attachment_block
    return new_description
