import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#download all resources from nltk
nltk.download('all')
#nltk.download('wordnet')
#nltk.download('stopwords')

# write the function of this python file and define all functionalities
def cleandata(data):
    # Read the CSV file into a Pandas dataframe
    df = data

    if df is None:
        return None

    # removing None values
    df = df.dropna(subset=['content'])

    # removing duplicate values
    df.drop_duplicates(subset=['content'], inplace=True)

    # Converting into lower case
    df['content'] = df['content'].str.lower()

    # Remove special characters
    def remove_special_characters(text):
        if isinstance(text, str):
            pattern = r'[^a-zA-Z\s]+'
            return re.sub(pattern, '', text)
        else:
            return text

    df.content = df.content.apply(lambda x: remove_special_characters(x))

    # Tokenization
    df['content_tokens'] = df['content'].astype(str).apply(nltk.word_tokenize)

    # Lemmatization
    lemmatizer = WordNetLemmatizer()

    def lemmatize(token_list):
        tokens = [lemmatizer.lemmatize(token) for token in token_list]
        return " ".join(tokens)

    df['cleaned_without_stopwords'] = df['content_tokens'].apply(lemmatize)

    # built-in stopword removal
    stop_words = set(stopwords.words('english'))  # Set of stopwords

    # function to remove stopwords from the text
    def remove_stopwords(text):
        if isinstance(text, str):
            # Remove URLs
            text = re.sub(r'http\S+|www\S+', '', text)
            # Remove stop words
            text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
        return text

    # apply the remove_stopwords function to the 'content' column
    df['cleaned'] = df['cleaned_without_stopwords'].apply(lambda x: remove_stopwords(x))

    # Export to a local csv file
    cleaned_filename = 'cleaned.csv'
    df.to_csv(cleaned_filename, index=True)

    return df