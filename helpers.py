import pandas as pd
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from commonHelpers import *

threshold = 0.01

def verify_patrols(patrols_data, wifi_data, locations, supabase_client):
    global locations_df
    task_df = get_task_df(patrols_data)
    locations_df = get_location_df(locations)
    total_locations = locations_df.shape[0]
    wifi_df = get_wifi_df(wifi_data)
    for _, row in task_df.iterrows():
        guard_phone = row["guard_phone"]
        shift = row["shift"]
        time_start, time_end = get_time_objects(shift, row["task_date"])
        bssids = wifi_df.loc[(wifi_df["created_at"] >= pd.Timestamp(time_start)) &  (wifi_df["created_at"] <= pd.Timestamp(time_end)) & (wifi_df["guard_phone"] == guard_phone), "bssid"].unique()
        ap_buckets = locations_df.loc[locations_df["ap_buckets"].apply(lambda x: len(set(x).intersection(set(bssids))) > 0), "patrol_loc"]
        len_locations = ap_buckets.shape[0]
        if len_locations > total_locations * threshold:
            supabase_client.table('tasks').update({"completed": True}).eq('id', row["id"]).execute()
            print("Patrol Verified and Database Updated!", guard_phone, shift, row["task_date"])
        else:
            print("Patrol Not Verified!", guard_phone, shift, row["task_date"])

def verify_monitors(monitors_data, wifi_data, locations, supabase_client):
    task_df = get_task_df(monitors_data)
    total_locations = locations_df.shape[0]
    wifi_df = get_wifi_df(wifi_data)
    for _, row in task_df.iterrows():
        guard_phone = row["guard_phone"]
        shift = row["shift"]
        time_start, time_end = get_time_objects(shift, row["task_date"])
        bssids = wifi_df.loc[(wifi_df["created_at"] >= pd.Timestamp(time_start)) &  (wifi_df["created_at"] <= pd.Timestamp(time_end)) & (wifi_df["guard_phone"] == guard_phone), "bssid"].unique()
        ap_buckets = locations_df.loc[locations_df["ap_buckets"].apply(lambda x: len(set(x).intersection(set(bssids))) > 0), "patrol_loc"]
        
        if row["location"] in ap_buckets.values:
            print("Verified Monitor")
            supabase_client.table('tasks').update({"completed": True}).eq('id', row["id"]).execute()
        else:
            print("Monitor Not Verified", guard_phone, shift, row["task_date"])
        # len_locations = ap_buckets.shape[0]
        # if len_locations > total_locations * threshold:
        #     supabase_client.table('tasks').update({"completed": True}).eq('id', row["id"]).execute()
        #     print("Patrol Verified and Database Updated!", guard_phone, shift, row["task_date"])
        # else:
        #     print("Patrol Not Verified!", guard_phone, shift, row["task_date"])
    



# supabase client
