from fastapi import FastAPI
from pydantic import BaseModel
from data_definer import dataSummary
import app_checks

app = FastAPI()


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
    data_obj = dataSummary(webhook)
    app_checks.url_check(data_obj)
    return data