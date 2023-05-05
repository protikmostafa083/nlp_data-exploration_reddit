import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import argparse

def get_df():
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, default='')

    # Parse the command-line arguments
    args, _ = parser.parse_known_args()

    # Get the value of the `--f` argument
    filename = args.f
    if not bool(filename):
        raise Exception('No value provided for --f when you run this program!')

    # Read the CSV file into a Pandas dataframe
    df = pd.read_csv(filename)
    return df

def main():
    df = get_df()
    #*************************************************** Cleaning the data ******************************************************************
    #-----------------------------------------------------Duplicate Values-------------------------------------------------------------------
    # For content column
    df.duplicated(['content']).value_counts()

    # Drop duplicates based on the "content" column
    df.drop_duplicates(subset=['content'], inplace=True)

    df.duplicated(['content']).value_counts()

    # ----------------------------------------------------- Missing Values-------------------------------------------------------------------
    # for content column
    df['content'].isnull().sum()

    # ------------------------------------------------ Converting into lower case
    df['content'] = df['content'].str.lower()

    # ------------------------------------------------ Remove special characters-------------------------------------------------------------------
    # define the function for removing special characters
    def remove_special_characters(text):
        if isinstance(text, str):
            pattern = r'[^a-zA-Z\s]+'
            return re.sub(pattern, '', text)
        else:
            return text

    # Applying the aforementioned function to the content columns
    df.content = df.content.apply(lambda x: remove_special_characters(x))

    # checking and droping duplicated values
    df.duplicated(['content']).value_counts()
    df.drop_duplicates(subset=['content'], inplace=True)

    # ------------------------------------------------ Remove stopwords-------------------------------------------------------------------
    stop_words = set(stopwords.words('english'))

    # add custom stop words to the set
    custom_stop_words = {"construction","working","building","workplace","someone","work","scaffolding","scaffold","site",\
                        "as","albeit","go","time","today","site","la","even","youre","he","said","do","using","shall","thing",\
                        "u","like","write","used","use","also","must","may","im","peter","based","various","nan","saw","etc","one","would"}
    stop_words = stop_words.union(custom_stop_words)

    # function to remove stopwords from the text
    def remove_stopwords(text):
        if isinstance(text, str):
            # Remove URLs
            text = re.sub(r'http\S+|www\S+', '', text)
            # Remove stop words
            text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
        return text

    # apply the remove_stopwords function to the 'content' column
    df['content'] = df['content'].apply(lambda x: remove_stopwords(x))

    # checking and droping duplicated values
    df.duplicated(['content']).value_counts()
    df.drop_duplicates(subset=['content'], inplace=True)

    # ------------------------------------------------Tokenization-------------------------------------------------------------------
    # Tokenize the content column using the nltk library
    df['content_tokens'] = df['content'].astype(str).apply(nltk.word_tokenize)

    # ------------------------------------------------Lemmatization-------------------------------------------------------------------
    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Define a function to lemmatize a list of tokens
    def lemmatize(token_list):
        tokens = [lemmatizer.lemmatize(token) for token in token_list]
        return " ".join(tokens)

    # Apply the lemmatize_tokens function to the content_token column
    df['lemmatized_content'] = df['content_tokens'].apply(lemmatize)
    df.rename(columns={'lemmatized_content': 'cleaned'}, inplace=True)
    df = df[['date', 'cleaned']]

    # Export to a local csv file
    df.to_csv('cleaned.csv')

if __name__ == "__main__":
    main()