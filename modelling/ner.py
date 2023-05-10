import streamlit as st
import pandas as pd
import spacy
import argparse
import subprocess
from modelling.summarization import summarize_dataframe


def install_model(model):
    subprocess.run(['python', '-m', 'spacy', 'download', model])


def get_ner(df, column, dataframe):
    # Check if en_core_web_sm model is installed, and install it if not
    # Display visualization using Streamlit
    st.header('Named Entity Recognition')
    st.subheader('To identify important people, places, events, and other entities mentioned in the posts.')

    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        st.write('Downloading language model... this may take a while')
        install_model('en_core_web_sm')
        nlp = spacy.load('en_core_web_sm')

    # Process the text with spaCy
    doc = nlp(df[column].str.cat(sep=' '))

    # Map SpaCy label to plain English
    label_map = {
        'PERSON': 'People',
        'NORP': 'Nationality/Interest Group',
        'FAC': 'Infrastructure',
        'ORG': 'Organization',
        'GPE': 'Country/City',
        'LOC': 'Location (Not Country/City)',
        'PRODUCT': 'Product',
        'EVENT': 'Event',
        'WORK_OF_ART': 'Literature',
        'LAW': 'Law',
        'LANGUAGE': 'Language',
        'MONEY': 'Money'
    }

    # Group the entities by label
    entities_by_label = {}
    for ent in doc.ents:
        label = ent.label_
        if label not in entities_by_label:
            entities_by_label[label] = []
        entities_by_label[label].append(ent.text)

    # Print the entities grouped by label with remapped labels
    for label, entities in entities_by_label.items():
        remapped_label = label_map.get(label, None)
        if remapped_label is not None:
            # use set() to remove duplicates
            st.write(remapped_label, list(set(entities)))

    # get the raw and summarized data from here
    selected_word2 = st.text_input("Enter a word to get the raw data and summarization:")
    df_selected_ner = dataframe[dataframe['content'].str.contains(selected_word2, na=False)]
    # Summarize the selected_word data
    summarize_dataframe(df_selected_ner, 'content', 1)

