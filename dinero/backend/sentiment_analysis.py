"""
Module: sentiment_analysis
This module provides functions for sentiment analysis of text data.

Function:
    - get_sentiment_value
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def get_sentiment_value(title_list: list) -> dict:
    """
    Analyzes the sentiment of each title in the given list using
    VADER (Valence Aware Dictionary and sEntiment Reasoner).

    Args:
    - title_list (list): A list of dictionaries representing titles or sentences to analyze.
                         Each dictionary should have 'title', 'content', and 'link' keys.

    Returns:
    - dict: A dictionary where keys are the titles/sentences and
            values are dictionaries containing sentiment scores.
            The sentiment scores include 'neg' (negative),
            'neu' (neutral), 'pos' (positive), and 'compound' (overall sentiment).
    """
    senti_dict = {}
    analyzer = SentimentIntensityAnalyzer()
    for sentence in title_list:
        content = sentence['content']
        title = sentence['title']
        link = sentence['link']
        sentiment_score = analyzer.polarity_scores(content)
        senti_dict[title] = {'sentiment_score': sentiment_score, 'link': link}

    return senti_dict
