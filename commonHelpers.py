import pandas as pd
import ast
import datetime 

def convert_to_ist(utc_time_str):
    # Replace the 'T' in the timestamp to space for datetime parsing
    utc_time_str = utc_time_str.replace('T', ' ')
    # Parse the string into a datetime object
    utc_time = pd.to_datetime(utc_time_str)
    # Add the UTC offset for IST (+05:30)
    ist_time = utc_time + pd.DateOffset(hours=5, minutes=30)
    return ist_time

def get_task_df(data):
    for entry in data:
        entry.pop('created_at', None)
        if 'personnel_list' in entry:
            guard_phone = entry['personnel_list'].get('guard_phone')
            entry['guard_phone'] = guard_phone
            entry.pop('personnel_list')
    df = pd.DataFrame(data)
    df = df[['id', 'shift', 'task_date', 'name', 'completed', 'task_type', 'location', 'guard_phone']]
    return df
def get_location_df(locations):
    for entry in locations:
        entry['ap_buckets'] = ast.literal_eval(entry['ap_buckets'])
    df = pd.DataFrame(locations)
    return df

def get_wifi_df(data):
    df = pd.DataFrame(data)
    df['created_at'] = df['created_at'].apply(convert_to_ist)
    return df
def get_time_objects(shift, date):
    if shift == "A":
        datetime_start = datetime.datetime.strptime(date + " 06:00:00", "%Y-%m-%d %H:%M:%S")
        datetime_end = datetime.datetime.strptime(date + " 14:00:00", "%Y-%m-%d %H:%M:%S")
    elif shift == "B":
        datetime_start = datetime.datetime.strptime(date + " 14:00:00", "%Y-%m-%d %H:%M:%S")
        datetime_end = datetime.datetime.strptime(date + " 22:00:00", "%Y-%m-%d %H:%M:%S")
    elif shift == "C":
        datetime_start = datetime.datetime.strptime(date + " 22:00:00", "%Y-%m-%d %H:%M:%S")
        datetime_end = datetime.datetime.strptime(date + " 06:00:00", "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
    return datetime_start, datetime_end