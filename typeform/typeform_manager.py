from logging_dir.logging import logger
from typeform import typeform_processing, typeform_data_points, image_manager
import jira_actions
import os


def boss(webhook):
    logger.info(f"Beginning Typeform processing....")
    # Parse the raw typeform response and create condensed block
    typeform_data_obj = typeform_processing.FromDataExtractor(webhook)
    typeform_data = typeform_data_obj.controller()
    # Create typeform data block - this is all we'll need from here on out
    typeform_app = typeform_data_points.typeformDataSummary(typeform_data)
    
    try:
        if not image_manager.image_consultant(typeform_app):
            return
    except Exception as err:
        raise err

    jira_key = jira_actions.find_jira_by_appid(typeform_app.app_id[0])

    if not jira_key:
        logger.info("Abandoning typeform autoamtion, no Jira ticket found.")
        return
    # Create subtask
    subtask = jira_actions.create_subtask(jira_key, typeform_app.app_name[0])
    # The name of the directory for where the app's images are stored - this is a dupe of imagemanager.folder_creator - this will need refactoring
    dir_name = (typeform_app.app_name[0].lower()).replace(" ", "_")
    # Get the list of files in the directory with modified app name
    files = image_manager.file_grabber(dir_name)
    # Build the full path to where the images are stored. 
    path = f"{os.getcwd()}/typeform/temp/{dir_name}/"
    # Add images to subtask
    jira_actions.add_images_to_jira(subtask, image_manager.file_list_creator(files, path))
    image_manager.clean_up(path)