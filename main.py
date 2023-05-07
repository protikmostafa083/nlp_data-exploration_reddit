import streamlit as st
import pandas as pd
import base64
import os
from DataCollection.praw_reddit_data_collector import RedditScraper
from EDA.dataClean import cleandata
from EDA.cleanpreviousfiles import cleanpreviousfiles
from modelling.wordcloud import generate_wordcloud
from modelling.maxminwords import get_max_min_words


st.set_page_config("Reddit Data Exploration", "🤖")
st.title('Reddit Search')

# clean the previous files from the file system
cleanpreviousfiles()

# Option to upload previous data
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")
    st.dataframe(data[['content', 'date']], width=650)
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
            st.dataframe(data[['content', 'date']])

            # add the download functionality
            if len(data) > 0:
                st.write("To download uncleaned the data, click the button below:")
                csv = data.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="reddit_data_uncleaned.csv"><button>Download Raw Data</button></a>'
                st.markdown(href, unsafe_allow_html=True)

if data is not None:
    # call the cleaning function
    #filename = cleandata(data)
    #cleandf = pd.read_csv(filename)
    cleandf = cleandata(data)

    # Display the cleaned data in a table
    st.write("Cleaned Data:")
    st.dataframe(cleandf[['cleaned', 'date']], width=650)

    # add the download functionality
    if len(cleandf) > 0:
        st.write("To download the cleaned data, click the button below:")
        csvclean = cleandf.to_csv(index=False)
        b64clean = base64.b64encode(csvclean.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64clean}" download="reddit_data_cleaned.csv"><button>Download Cleaned Data</button></a>'
        st.markdown(href, unsafe_allow_html=True)

    # Generate and display the wordcloud
    st.subheader("Wordcloud")

    text = ' '.join(cleandf['cleaned'].astype(str).tolist())

    # Display the wordcloud
    generate_wordcloud(text)  # Set max_words to a fixed value of 100

    # Show top and bottom 10 words
    st.subheader("Top and least 10 words")
    fig = get_max_min_words(cleandf, 'cleaned')
    st.plotly_chart(fig)
else:
    st.write("Nothing to show now. Search or upload file first")
