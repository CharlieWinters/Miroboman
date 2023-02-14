from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from shared import data_definer, controller
from jira import app_validator
import json
import uuid
from jira import passed_checks
from logging_dir.logging import logger
from typeform import typeform_manager
import config

app = FastAPI()

success = json.dumps({'success': True}), 200, {'Content-Type': 'application/json'}
bad_request = json.dumps({'success': False}), 400, {'Content-Type': 'application/json'}

# Middleware to add unique hash to each request for easier logging
@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id):
        logger.info(f"Request started for {request_id}")

        try:
            response = await call_next(request)

        except Exception as ex:
            logger.error(f"Request failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)

        finally:
            response.headers["X-Request-ID"] = request_id
            logger.info(f"Request ended for {request_id}")
            return response


# Root route
@app.get("/")
async def root():
    logger.info(f"Someone hit the root. Miro is running on {config.env}")
    return {"message": "Miroboman reporting for duty!"}

# Data model for app reviews
class Data(BaseModel):
    issue_key: str
    app_name: str
    summary: str
    # removed description due to https://github.com/CharlieWinters/Miroboman/issues/3
    #description: str
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
    app = data_definer.dataSummary(webhook)
    logger.info(f"New app submission received with ticket number {app.issue_key}")
    app_check_result = app_validator.appComponentCheck(app)
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

@app.post("/in-progress")
def read_item(data: Data):
    logger.info(f"App review started")
    webhook = data
    app = data_definer.dataSummary(webhook)
    logger.info(f"App review started for {app.issue_key}")
    controller.app_review_started(app)
    return success


# Typeform 
@app.post("/typeform_submission")
async def typeform_processor(request: Request):
    webhook = await request.json()
    logger.info(f"New Typeform submission")
    typeform_manager.boss(webhook)
    return success
