from pprint import pprint
from sentiment_analysis import get_sentiment_value
from req import get_news_articles
from transform import get_filter_dates



sentiment_date = {}

dates_dictionary = get_filter_dates("/Users/stlp/Documents/data557/final_project/dinero/data/AAPL.csv",5, "AAPL")

pprint(dates_dictionary)


for key,value in dates_dictionary.items():
    
    sentiment_date[key] = get_sentiment_value(value)
    
pprint(sentiment_date)