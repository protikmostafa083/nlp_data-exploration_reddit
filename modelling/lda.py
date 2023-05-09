import streamlit as st
import gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

cleaned_col = 'cleaned'


def get_lda(df, column):
    # Extract the 'content' column as a list of sentences
    data = [str(sent).split() for sent in df[column].tolist()]

    # Create dictionary and corpus
    dictionary = gensim.corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(doc) for doc in data]



    # Display visualization using Streamlit
    st.header('Latent Dirichlet Allocation (LDA Topic Model)')
    st.subheader('To categorize large volumes of text data into meaningful groups of topic.')
    st.markdown('*\*a topic means a set of words that frequently co-occur in a collection of posts.*')

    # Explanation of visualization features
    st.markdown(
        '1. Each bubble represents an identified topic. **The larger the bubble, the higher percentage of the number of posts in the corpus is about that topic**.')
    st.markdown(
        '2. Blue bars represent the overall frequency of each word in the corpus. If no topic is selected, the blue bars of the most frequently used words will be displayed.')
    st.markdown('3. Red bars represent the frequency of word within the selected topic.')
    st.markdown('4. **The further the bubbles are away from each other, the more different they are**.')
    st.markdown(
        '5. When relevance metric slider is set for λ = 1 (by default), it sorts words by their frequency within the specific topic (by their red bars).')
    st.markdown(
        '6. By contrast, setting λ = 0 words sorts words whose red bars are nearly as long as their blue bars will be sorted at the top.')

    # Build LDA model
    # Add a slider for the number of topics
    num_topics = 0
    num_topics = st.slider('Select the number of topics:', min_value=2, max_value=10, value=4)
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)


    # Visualize topics
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary, R=10)
    html_string = pyLDAvis.prepared_data_to_html(vis_data)
    st.components.v1.html(html_string, width=1500, height=1000, scrolling=True)
