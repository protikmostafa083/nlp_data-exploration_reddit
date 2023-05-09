import streamlit as st
import pandas as pd
import spacy
import argparse
import subprocess


def install_model(model):
    subprocess.run(['python', '-m', 'spacy', 'download', model])


def get_ner(df, column):
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


