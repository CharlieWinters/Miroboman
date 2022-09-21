from fastapi import FastAPI, Request
from pydantic import BaseModel
from data_definer import dataSummary
from app_validator import appComponentCheck
import json
import passed_checks
from logging_dir.logging import logger
from typeform import typeform_manager

app = FastAPI()

# Function to initiate logging
def logger_initiation():
    logger.info("Miroboman is starting up.")

success = json.dumps({'success': True}), 200, {'Content-Type': 'application/json'}
bad_request = json.dumps({'success': False}), 400, {'Content-Type': 'application/json'}
logger_initiation()

# Root route
@app.get("/")
async def root():
    return {"message": "Markitman reporting for duty!"}

# Data model for app reviews
class Data(BaseModel):
    issue_key: str
    app_name: str
    summary: str
    description: str
    user_id: str
    app_id: str
    setup_instructions: str
    scopes: str
    installation_url: str
    recording_link: str
    integration_credentials: str

# Data model for typeform
class FormData(BaseModel):
    payload: dict

# App review route
@app.post("/review")
def read_item(data: Data):
    webhook = data
    app = dataSummary(webhook)
    logger.info(f"New app submission received with ticket number {app.issue_key}")
    app_check_result = appComponentCheck(app)
    if app_check_result.controller():
        # App has passed initial checks | Do more stuff.
        logger.info("App passed initial checks, sending welcome message.")
        passed_checks.welcomeActions(app)
        logger.info("Actions complete, app ready for review.")
        return success
    else:
        # App has failed initial checks | do more stuff. 
        logger.info("Placeholder comment - App failed initial checks, exiting out of review process.")
        return success


# Typeform 
@app.post("/typeform_submission")
async def typeform_processor(request: Request):
    webhook = await request.json()
    logger.info(f"New Typeform submission")
    #print(webhook)
    typeform_manager.boss(webhook)
    #typeform_processing.url_extractor(typeform_data)
    return success
