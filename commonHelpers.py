import pandas as pd
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
