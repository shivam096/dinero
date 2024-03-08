import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment_value(title_list: list) -> dict:
    senti_dict = {}
    analyzer = SentimentIntensityAnalyzer()
    for sentence in title_list:
        vs = analyzer.polarity_scores(sentence)
        senti_dict[sentence] = vs
    
    return senti_dict