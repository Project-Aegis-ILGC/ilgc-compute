import pandas as pd
from dotenv import load_dotenv
import os
from supabase import create_client, Client

def verify_patrols(patrols_data, wifi_data):
    print(get_task_df(patrols_data))
load_dotenv()
def get_task_df(data):
    for entry in data:
        entry.pop('created_at', None)
        if 'personnel_list' in entry:
            guard_phone = entry['personnel_list'].get('guard_phone')
            entry['guard_phone'] = guard_phone
            entry.pop('personnel_list')

    # Create DataFrame
    df = pd.DataFrame(data)

    # Rearrange columns to exclude 'created_at' and include 'guard_phone'
    df = df[['shift', 'task_date', 'name', 'timecompletion', 'task_type', 'location', 'guard_phone']]
    return df


# supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
uncompleted_patrols = supabase.table('tasks').select("*, personnel_list(guard_phone)").eq('task_type', 'Patrol').is_('timecompletion', "null").execute().data
wifi_conn = supabase.table('wifi_connections').select("*").execute().data

print(verify_patrols(uncompleted_patrols, wifi_conn))
    
