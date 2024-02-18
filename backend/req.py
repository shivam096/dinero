import requests

def get_news_articles(ticker : str, date: str) :
    url = f'https://eodhd.com/api/news?s={ticker}&offset=0&api_token=demo&fmt=json&from={date}&to={date}'
    data = requests.get(url).json()
    return data