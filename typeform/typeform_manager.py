from logging_dir.logging import logger
from typeform import typeform_processing, typeform_data_points, image_manager



def boss(webhook):
    logger.info(f"Beginning Typeform processing....")
    # Parse the raw typeform response and create condensed block
    typeform_data_obj = typeform_processing.FromDataExtractor(webhook)
    typeform_data = typeform_data_obj.controller()
    # Create typeform data block - this is all we'll need from here on out
    typeform_app = typeform_data_points.typeformDataSummary(typeform_data)
    try:
        image_manager.image_consultant(typeform_app)
    except Exception as err:
        raise err
