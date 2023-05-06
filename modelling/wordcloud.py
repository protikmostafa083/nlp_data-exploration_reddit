import matplotlib

from wordcloud import WordCloud
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def generate_wordcloud(text):
    """
    Function to generate a wordcloud from text data.
    :param text: str, the text data to generate the wordcloud from.
    """

    # Create a wordcloud object
    wc = WordCloud(
        width=800,                     # Width of the wordcloud image
        height=400,                    # Height of the wordcloud image
        background_color='white',      # Background color of the wordcloud image
        colormap='tab10',              # Colormap used to color the wordcloud image
        max_words=200                  # Maximum number of words to include in the wordcloud
    )

    # Generate wordcloud from the text
    wc.generate(text)

    # Display the wordcloud
    plt.figure(figsize=(12, 6))       # Set the figure size of the plot
    plt.imshow(wc, interpolation='bilinear')  # Plot the wordcloud image
    plt.axis('off')                  # Turn off the axes of the plot
    plt.tight_layout(pad=0)          # Set the padding of the plot
    plt.show()                       # Display the plot
