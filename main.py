import streamlit as st
import pandas as pd
from DataCollection.praw_reddit_data_collector import RedditScraper

st.set_page_config("Reddit Data Exploration", "🤖")

st.title('Reddit Search')
# Option to upload previous data
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")
    st.dataframe(data[['subreddit', 'username', 'url', 'content', 'upvotes', 'date']])
    # Hide search options if file is uploaded
    st.experimental_set_query_params(file_uploaded="true")
else:
    data = None
    # Show search options if file is not uploaded
    if st.experimental_get_query_params().get("file_uploaded") != "true":
        st.warning("Please upload a CSV file or run a new search.")
        search_query = st.text_input('Enter your search query:')
        time_filters = ['all', 'day', 'hour', 'month', 'week', 'year']
        time_filter = st.selectbox('Choose a time filter:', time_filters, index=0)
        sort_methods = ['relevance', 'hot', 'top', 'new', 'comments']
        sort_method = st.selectbox('Choose a sort method:', sort_methods, index=0)
        if st.button('Search'):
            scraper = RedditScraper(time_filter=time_filter, sort_method=sort_method)
            scraper.run(search_query, 'reddit_data.csv')
            # Load the saved data
            data = pd.read_csv('reddit_data.csv')
            # Display the data in a table
            st.dataframe(data[['subreddit', 'username', 'url', 'title', 'content', 'upvotes', 'date']])
    else:
        # Display the data
        st.dataframe(data[['subreddit', 'username', 'url', 'title', 'content', 'upvotes', 'date']])
