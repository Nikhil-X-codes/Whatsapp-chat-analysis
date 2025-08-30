import re
import pandas as pd

def pre(data):                                                                                          
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        'message_date': dates,
        'user_message': message
    })
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for mess in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', mess)  
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group notification")
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # Strip whitespace from messages and users before filtering
    df['message'] = df['message'].astype(str).str.strip()
    df['user'] = df['user'].astype(str).str.strip()
    
    # More comprehensive filtering for deleted/empty messages
    df = df[~df['message'].isin(['This message was deleted', '', ' '])]
    df = df[~df['message'].str.contains(r'^\s*$', na=False)] 

    df = df[~df['user'].str.contains('You joined a group', na=False)]
    
    # Reset index after filtering
    df = df.reset_index(drop=True)
    
    return df
