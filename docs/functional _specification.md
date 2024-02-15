
# Functional Specification

## Background. 

In the realm of financial markets, data has become the lifeblood of informed decision-making and strategic investment. The ability to harness and analyze vast streams of data has become increasingly crucial for investors seeking to navigate the complex landscape of stocks, bonds, and other financial instruments.

In this context, the project aims to create a comprehensive platform for analyzing stock market data, with a focus on identifying trends, exploring historical patterns, and extracting actionable insights for investment decision-making. By leveraging a combination of statistical analysis, technical indicators, natural language processing (NLP), and interactive visualization techniques, the platform seeks to empower users with the tools and information needed to make informed investment choices.

The project draws upon the wealth of data available from sources such as Yahoo Finance and EODHD APIs, which provides access to historical stock prices, company fundamentals, and news articles related to financial markets. By integrating these disparate datasets and applying advanced analytics techniques, the platform aims to uncover hidden patterns, correlations, and relationships that can inform investment strategies and enhance portfolio performance.

## User profile. 

### Individual Investors (General/Novice User)

- Linda is a new investor in stock market.
- She wants to see the visualization of stock trends.
- She wants to see trading activities for specific companies.
- She wants to interact with the stock information with filters or simple text input.
- She has limited financial knowledge and is not a technical person.
- She needs a user friendly interface.

### Financial Analysts / Professional Traders (Power User)

- Mark is a trader working in investment firm.
- He wants to see the overview of trading activities in the stock market.
- He wants to check the KPIs and technical indicators for specific companies.
- He wants to track stock trendsa and compare news, to see the rise or fall in daily stocks and use that information.
- He wants to search for a summary of relevent events and keywords from news and how would these events impact on stock market.
- He knows terms in stock market but does not have technical skills.
- He needs a simple user interface.

### Data Analysts / Market Researchers (Power User)

- Jennifer is a data scientist interested in studying market dynamics, investor behavior, and the impact of news events on stock prices.
- She wants access to comprehensive datasets and advanced analytics capabilities for building and testing trading algorithms.
- She wants to conduct empirical studies, hypothesis testing, and generating insights for academic publications or industry reports.
- She has adequate knowledge in both stock market and technology field.
- She can use user friendly interface or function calls.

### Development Team

- Robert is a developer.
- He is continually supporting and maintaining and updating database, including the sentiment analysis model and KPI metrics.
- He responds to the feedback from users and improves user experience. 
- He is in charge of debugging the application.
- He is highly technical and knows programming. 
- He uses an IDE to interact with the backend, makes API calls to fetch the data and update the database.

## Data sources. 

This project utilizes the [Yahoo Finance](https://finance.yahoo.com/) open-source API and [EODHD](https://eodhd.com/?utm_source=google_ads&utm_medium=cpc&utm_campaign=us_reborn_&utm_content=us_generic&utm_term=financial%20data%20apis&gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgTVWuR3EPPyvNhiJhll2IfgY-f3bSVNVy3Ll0YRi9-XW7SRaAzwDaoaAtmHEALw_wcB) API to access relevant data for our analysis.

1. **Company Stock Price**: This static dataset retrieves historical stock data from Yahoo for key metrics like open price, close price, volume, and adjusted price for the chosen companies and timeframe.

2. **Stock Market and Financial News**: This dataset is biult on EODHD news API, retrieving news articles and events related to the specific companies within the defined date range. Each news item in this dataset will include information like title, date, content, and original URL, enabling further exploration and analysis.

## Use cases. 

### Objective 1: System displays stock data visualization based on user-selected filters

User: Accesses the main page
System: Displays the data visualization pertaining to the entire dataset (all companies, all date ranges, etc.)
User: Selects events, filters date ranges, and/or selects companies
System: Displays the stock data visualization pertaining to the user-selected filters

### Objective 2: System displays news pertaining to relevant events (drastic changes in the stock data)

User: Clicks on a data point on the interactive data visualization of the stock data on the main page
System: Displays the event and relevant news

### Objective 3: System displays KPIs of interest to the user for specific stocks

User: Accesses the main page where the filter by company is selected. User clicks a button for the technical indicator of interest and company stock
System: Displays the technical indicator of interest and company stock