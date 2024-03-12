# dinero
Repository for *DATA 515 : Software Design for Data Scientists*

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

## Dataset
This project utilizes the [Yahoo Finance](https://finance.yahoo.com/) open-source API to access relevant data for our analysis. We employ two distinct API calls to acquire two primary datasets:

1. **Company Stock Data:** This static dataset retrieves historical values for key metrics like open price, close price, volume, and adjusted price for the chosen companies and timeframe.

2. **News and Events:** This call retrieves a dynamic dataset of news articles and events related to the specific companies within the defined date range. Each news item in this dataset will include information like title, summary, and original URL, enabling further exploration and analysis.
