
from textblob import TextBlob
def calculate_sentiment(text):
    return TextBlob(text).sentiment.polarity