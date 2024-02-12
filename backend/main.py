from req import get_news_articles
from transform import find_count_value_change


dates_for_articles = find_count_value_change("/Users/stlp/Documents/data557/final_project/dinero/data/AAPL.csv",5)


news_articles_links = {}

for date in dates_for_articles:
    
    news_articles_links[date] = get_news_articles('AAPL',date=date)

print(news_articles_links)