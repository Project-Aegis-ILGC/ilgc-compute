from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time
import pandas as pd
from helpers import *
from commonHelpers import *
# load .env files
load_dotenv()

# supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# fastapi app

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

def verify():
    uncompleted_patrols = supabase.table('tasks').select("*, personnel_list(guard_phone)").eq('task_type', 'Patrol').eq('completed', False).execute().data
    wifi_conn = supabase.table('wifi_connections').select("*").execute().data
    locations = supabase.table('locations').select("*").execute().data
    uncompleted_monitors = supabase.table('tasks').select("*, personnel_list(guard_phone)").eq('task_type', 'Monitor ').eq('completed', False).execute().data
    loc = get_location_df(locations)
    if len(uncompleted_monitors) != 0:
        verify_monitors(uncompleted_monitors, wifi_conn, loc, supabase)
    if len(uncompleted_patrols) != 0:
        verify_patrols(uncompleted_patrols, wifi_conn, loc, supabase)
    


while True:
    verify()
    print("Verfiying...")
    time.sleep(1)