import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# uploads file and converts into readable dataframe format
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.pre(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis For",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,num_words,num_media_messages,num_links = helper.stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

# create columbs for each stats and display them in the app

    if selected_user == 'Overall':
        st.title("Most Busy Users")
        x,new_df= helper.most_busy_users(df)
        fig,ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
         ax.bar(x.index, x.values,color='red')
         plt.xticks(rotation=45, ha='right')
         st.pyplot(fig)

        with col2:
         st.dataframe(new_df)



    st.title("Wordcloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)



    emoji_df = helper.emojis(selected_user,df)
    st.title("Emoji Analysis")
    
    st.dataframe(emoji_df) 

    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(timeline['time'], timeline['message'], color='green')

    plt.xticks(rotation=45, ha='right')

    ax.set_xticks(timeline['time'][::2]) 

    st.pyplot(fig)






    



    