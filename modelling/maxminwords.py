import pandas as pd
from collections import Counter
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def get_max_min_words(df, col):
    """
    Function to get the top 10 and bottom 10 occurring words in a given column of a dataframe
    :param df: pandas.DataFrame, the dataframe containing the text column
    :param col: str, the name of the text column
    :return: plotly.graph_objs.Figure, a figure object showing the 10 most and least frequent words side by side
    """
    # Create a list of all words in the column
    words_list = df[col].str.split(expand=True).stack().tolist()

    # Count the frequency of each word
    word_counts = dict(Counter(words_list))

    # Get the top 10 and bottom 10 most frequent words
    top10 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    bottom10 = dict(sorted(word_counts.items(), key=lambda x: x[1])[:10])

    # Create the plotly subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Top 10 Words', 'Bottom 10 Words'))

    # Add bar traces for top 10 words subplot
    fig.add_trace(go.Bar(x=list(top10.keys()), y=list(top10.values()), name='Most frequent words'), row=1, col=1)

    # Add bar traces for bottom 10 words subplot
    fig.add_trace(go.Bar(x=list(bottom10.keys()), y=list(bottom10.values()), name='Least frequent words'), row=1, col=2)

    # Update layout of the figure
    fig.update_layout(title='Top and bottom 10 words', barmode='group')

    return fig
