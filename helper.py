from urlextract import URLExtract

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
