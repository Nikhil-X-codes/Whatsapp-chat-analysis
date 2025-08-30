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
