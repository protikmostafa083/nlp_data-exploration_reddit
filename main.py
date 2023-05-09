import streamlit as st
import pandas as pd
import base64
import os
from DataCollection.praw_reddit_data_collector import RedditScraper
from EDA.dataClean import cleandata
from EDA.cleanpreviousfiles import cleanpreviousfiles
from modelling.wordcloud import generate_wordcloud
from modelling.maxminwords import get_max_min_words
from EDA.customstopword import remove_custom_stopwords
# from modelling import Concordance, LDA, NER, NGrams
from modelling.concordance import get_concordance
from modelling.lda import get_lda
from modelling.ner import get_ner
from modelling.ngrams import get_ngrams
from modelling.summarization import summarize_dataframe



st.set_page_config("Reddit Data Exploration", "🤖", layout='wide')
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
        if search_query != '' and time_filter != '' and sort_method != '':
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

    # Remove custom stop words
    custom_stop_words = st.text_input("Enter comma-separated words to remove from the text:")
    if custom_stop_words:
        stop_words_list = [word.strip() for word in custom_stop_words.split(",")]
        remove_custom_stopwords(cleandf, stop_words_list)
        st.success(f"Removed custom stop words: {stop_words_list}")
    # Generate and display the wordcloud
    # Generate and display the wordcloud
    st.subheader("Wordcloud")
    text = ' '.join(cleandf['cleaned'].astype(str).tolist())
    max_words = st.slider("Max Words", 50, 300, 100)
    generate_wordcloud(text, max_words)

    # Show top and bottom 10 words
    st.subheader("Top and least 10 words")
    fig = get_max_min_words(cleandf, 'cleaned')
    st.plotly_chart(fig)

    # show the other modelling
    modelling = st.selectbox('Select model', ['Concordance', 'LDA', 'NER', 'NGrams', 'Summarization'])
    if modelling == 'Concordance':
        st.header('Concordance')
        st.subheader('To show the context surrounding a particular word in a post.')

        # Explanation of visualization features
        st.write('1. Enter a single keyword.')
        st.write(
            '2. The result allows you to see all the instances of the word in all the posts, along with the words immediately preceding and following it.')
        st.write(
            '3. By examining the context in which a word appears, it may be possible to **determine its intended/broader meaning of the word** in the post.')

        # Add a text input box for the user to enter the input word
        input_word = st.text_input("Enter a word for concordance:")
        if input_word:
            st.write(f"Concordance associated with '{input_word}':")
            #num_words = st.slider('Number of words', 1, 200, 30)
            result = get_concordance(cleandf, "cleaned", input_word, num_words=40)
            for line in result:
                st.markdown(line, unsafe_allow_html=True)
        else:
            st.write("Please enter a word for concordance.")
    elif modelling == 'LDA':
        get_lda(cleandf, 'cleaned')
    elif modelling == 'NER':
        get_ner(cleandf, 'cleaned')
    elif modelling == 'NGrams':
        get_ngrams(cleandf, 'cleaned')
    elif modelling == 'Summarization':
        summarize_dataframe(data,'content', 1)


else:
    st.write("Nothing to show now. Search or upload file first")
