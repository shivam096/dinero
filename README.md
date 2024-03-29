# dinero
Repository for *DATA 515 : Software Design for Data Scientists*

![Build/Test Workflow](https://github.com/shivam096/dinero/actions/workflows/build_test.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/shivam096/dinero/badge.svg?branch=main)](https://coveralls.io/github/shivam096/dinero)

## Project Type
 Creating Reusable Data

## Questions of Interest
1. Can company stock data be use to explore trends and view seasonal changes, allowing us to leverage this knowledge for deeper analysis?

2. Can we leverage statistical data and historical data to calculate different technical indicators (like MACD and RSI) to identify profitable trading opportunities for specific company profiles?

3. What are the Top 5 events that affected stock prices? How does the stock price response to different types of news events (e.g., earnings releases, political announcements, etc) ?

4. Can we use natural language processing (NLP) techniques to analyze news articles and identify sentiment (positive, negative, neutral) associated with specific companies or events, and further correlate those sentiments with stock price movements?
Additionally, which keywords are most associated with significant events and their corresponding sentiment?

## Goals for Project

1.  Analyze stock data for **five** chosen companies to provide focused insights.
3.  Design a **user-friendly interface** that facilitates navigation between functionalities and allows visualization of stock data to identify patterns and anomalies.
5.   Implement **filters** for company selection, date range, event type, and sentiment analysis, and offer meaningful insights based on the chosen criteria.
7.   Define company-specific **key performance indicators (KPIs)** derived from historical data. Integrate various technical indicators (e.g., MACD, RSI) for a comprehensive technical analysis applicable to all companies.
9.  Display **headlines of news events** affecting chosen companies alongside their impact on stock prices.
11.  Show the **sentiment and keywords** associated with news events and analyze the correlation between news sentiment and stock price movements.

### Stretch Goals
 1. Analyzing how our technical indicators compare to existing market forecasts in terms of effectiveness and performance.
 2. Extending our study of interest to more than 5 companies

## Data sources. 

This project utilizes the [Yahoo Finance](https://finance.yahoo.com/) open-source API and [EODHD](https://eodhd.com/?utm_source=google_ads&utm_medium=cpc&utm_campaign=us_reborn_&utm_content=us_generic&utm_term=financial%20data%20apis&gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgTVWuR3EPPyvNhiJhll2IfgY-f3bSVNVy3Ll0YRi9-XW7SRaAzwDaoaAtmHEALw_wcB) API to access relevant data for our analysis.

1. **Company Stock Price**: This static dataset retrieves historical stock data from Yahoo for key metrics like open price, close price, volume, and adjusted price for the chosen companies and timeframe.

2. **Stock Market and Financial News**: This dataset is biult on EODHD news API, retrieving news articles and events related to the specific companies within the defined date range. Each news item in this dataset will include information like title, date, content, and original URL, enabling further exploration and analysis.

## Technical dependency
The application supports only Python versions 3.9 and 3.10. Python 3.11 incorporation is still in the works.
