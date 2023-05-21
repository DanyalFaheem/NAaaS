from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment_tb(text):
    """
    This function takes a paragraph as string and returns the sentiment analysis 
    on the scale of 0 to 1, where 0 means most negative and 1 means really good.
    """
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    normalized_score = (sentiment_score + 1) / 2  # Normalize the score to a range of 0 to 1
    return normalized_score

def get_sentiment_nl(text):
    """
    This function takes a paragraph as string and returns the sentiment analysis 
    on the scale of 0 to 1, where 0 means most negative and 1 means really good.
    """
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    normalized_score = (compound_score + 1) / 2  # Normalize the score to a range of 0 to 1
    return normalized_score

def get_sentiment(text):
    scoretb = get_sentiment_tb(text)
    scorenl = get_sentiment_nl(text)
    final_score = ((scorenl + scoretb)) / 2
    return final_score 
