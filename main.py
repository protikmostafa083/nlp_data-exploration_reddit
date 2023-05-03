import streamlit as st
import pandas as pd
from DataCollection.praw_reddit_data_collector import RedditScraper

st.title('Reddit Search')

search_query = st.text_input('Enter your search query:')
time_filters = ['all', 'day', 'hour', 'month', 'week', 'year']
time_filter = st.selectbox('Choose a time filter:', time_filters, index=0)
sort_methods = ['relevance', 'hot', 'top', 'new', 'comments']
sort_method = st.selectbox('Choose a sort method:', sort_methods, index=0)
if st.button('Search'):
    scraper = RedditScraper(time_filter=time_filter, sort_method=sort_method)
    scraper.run(search_query, 'reddit_data.csv')

    # Load the saved data and display it in a table
    data = pd.read_csv('reddit_data.csv')
    st.write(data)
