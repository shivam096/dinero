import requests
from bs4 import BeautifulSoup
import openai

openai.api_key = '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'

def scrape_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract article content
        article_content = soup.find('article').get_text() if soup.find('article') else ""
        return article_content
    else:
        print("Failed to fetch content from the website.")
        return None



website_url = "https://finance.yahoo.com/m/e3796386-695a-31e3-b0f9-65d0cea42e79/history-says-the-nasdaq-could.html"
article_content = scrape_website_content(website_url)
print(article_content)
# if article_content:
#     keywords = extract_keywords(article_content)
#     summary = summarize_article(article_content)
#     print("Keywords:", keywords)
#     print("Summary:", summary)
