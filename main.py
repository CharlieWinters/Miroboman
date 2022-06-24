from fastapi import FastAPI
from pydantic import BaseModel
from data_definer import dataSummary
from app_validator import appComponentCheck
import json

app = FastAPI()

success = json.dumps({'success': True}), 200, {'Content-Type': 'application/json'}
bad_request = json.dumps({'success': False}), 400, {'Content-Type': 'application/json'}

# Root route
@app.get("/")
async def root():
    return {"message": "Markitman reporting for duty!"}

# Data model for app reviews
class Data(BaseModel):
    issue_key: str 
    summary: str
    description: str
    user_id: str
    app_id: str
    setup_instructions: str
    scopes: str
    installation_url: str
    project_link: str
    recording_link: str

# App review route
@app.post("/review")
def read_item(data: Data):
    webhook = data
    app = dataSummary(webhook)
    if appComponentCheck(app):
        # App has passed initial checks | Do more stuff.
        print("Placeholder comment - App passed initial checks")
    else:
        # App has failed initial checks | do more stuff. 
        print("Placeholder comment - App failed initial checks")
    return data