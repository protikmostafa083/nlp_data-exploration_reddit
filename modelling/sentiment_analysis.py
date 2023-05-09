from textblob import TextBlob
import plotly.express as px
import streamlit as st


# define function to get sentiment analysis and visualize it.
def get_sentiment(sentence):
    blob = TextBlob(sentence)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"


def plot_sentiment_analysis(df, column_name):
    df['sentiment'] = df[column_name].apply(get_sentiment)
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']

    # Specify the color of the bars based on sentiment
    color_discrete_map = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'yellow'}

    fig = px.bar(sentiment_counts, x='sentiment', y='count',
                 color='sentiment', color_discrete_map=color_discrete_map)

    # Add a legend to the plot
    fig.update_layout(title='Sentiment Analysis of {}'.format(column_name),
                      legend_title='Sentiment')
    st.plotly_chart(fig)
