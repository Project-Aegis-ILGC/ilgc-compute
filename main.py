from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import helpers
# load .env files
load_dotenv()

# supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# fastapi app
app = FastAPI()


# # schedule process_data to run every 60 seconds
# scheduler = BackgroundScheduler()
# scheduler.add_job(process_data, 'interval', seconds=60)
# scheduler.start()

# get excel sheet
# @app.get("/excel")
# def get_excel():
#     # patrols = supabase.table('tasks').select("*, personnel_list(rank)").eq('task_type', 'Patrol').execute().data
#     # return patrols
#     return {"data": "i am an excel sheet"}

# @app.get("/")
# def show_nothing():
#     return "I am showing nothing"

@app.get("/verify")
def verify_patrols():
    uncompleted_duties = supabase.table('tasks').select("*, personnel_list(guard_phone)").neq('task_type', 'Patrol').is_('timecompletion', "null").execute().data
    wifi_conn = supabase.table('wifi_connections').select("*").execute().data
    response = helpers.verify_duties(uncompleted_duties, wifi_conn)
    return wifi_conn