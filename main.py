from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

# load .env files
load_dotenv()

# supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# fastapi app
app = FastAPI()


# process data function
def process_data():
    print("Yo")

# schedule process_data to run every 60 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(process_data, 'interval', seconds=60)
scheduler.start()

# get excel sheet
@app.get("/excel")
def get_excel():
    return {"Hello": "World"}
