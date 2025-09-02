from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def stats(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    num_messages = df.shape[0]
    
    words = []
    for message in df['message']:
        words.extend(str(message).split())
    
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    
    links = []
    for message in df['message']:
       links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links) 
   
# return no of messages, no of words, no of media messages, no of links
  
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df= round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
     df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def emojis(selected_user, df):
   
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis_list = []

    for mess in df['message']:
        emojis_list.extend([c for c in mess if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis_list).most_common(len(Counter(emojis_list))),
                            columns=['emoji', 'count'])
    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_name']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
     time.append(str(timeline['month_name'][i]) + " " + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def weekly_timeline(selected_user, df):
   
    if selected_user != 'Overall':
      df = df[df['user'] == selected_user]

    weekline = df.groupby('day_name').count()['message'].reset_index()

    return weekline

def month_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if df.empty:
        return None   

    monthly_timeline = df.groupby(['month', 'month_name']).count()['message'].reset_index()
    monthly_timeline = monthly_timeline.sort_values('month') 

    return monthly_timeline


def day_map(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap




   
   

