# Component Specification

The system consists of three components that interact with each other accross database, backend and front end.

![System Workflow](https://github.com/shivam096/dinero/blob/main/docs/images/System_design.png)

## Component 1. User Interface

### Overview

The UI component creates interactive web applications and builds intuitive and visually appealing user interfaces using `streamlit` Python Package.

### Implementation
A single `app.py` file.

### Sub-component 1 UI Filters and Input Boxes

The Filters and Input Boxes implements interactivity to web applications.

#### Interations

Interact with two other components: *Backend Stock Data Processor* and *Bakend News Data Processor* by
- passing inputs to retreive data from the backend.
- displaying the plots and sentiment scores from the backend.

#### Key Functions
1. Company Filter

**what it does**:
Facilitate user interaction to display graphs, and news articles specific to a chosen company.

**Input**: User selects a company from a predefined dropdown menu on the user interface.
Internally, the input is a string representing the selected company from a pre-defined list. This string is passed to various functions responsible for generating visualizations and displaying data.

**Assumptions**:
Users are familiar with the companies available in the dropdown menu.

2. Input Boxes

**what it does**:
Facilitate user interaction to run sentiment analysis model and display the results.

**Input**: User input strings or integers as instructed on the web page.

### Sub-component 2 UI Design and Layout 

The Design and Layout component builds intuitive and visually appealing user interfaces.

**Usage**:
The tab functionality in `streamlit` enables users to easily switch between different categories of information. Each tab can contain distinct sets of components and functionality tailored to its specific purpose.

**Pseudocode**:
```
tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])

with tab1:
    # Remaining code for Tab 1

with tab2:
    # Remaining code for Tab 2
```

**Usage**: The Streamlit Expander allows for the collapsible display of additional content within a section. It helps to maintain a clean and organized layout by initially displaying only essential information, with the option to reveal additional details as needed.

**Sample Code**:
```
with st.expander("News Headline"):
    st.write("News Article")
```

## Component 2. Backend Stock Price Procesor

### Sub-component 1 Stock Data Manager

#### Overview

The Stock Data Manager component is designed to build the static database by extracting stock data from Yahoo Finance and grant access to it.

#### Interaction with Other Components

Interacts with all other components across frondend and backend.

#### Modules
1. `backend.stock_data_manager`

#### Key Functions
1. `download_stock_data`

**what it does**: Collect stock data specified by company name and time through yfinance API call. Create a `csv` file containing Date, Open, High, Low, Close, Adj Close, Volume.

**Input**: `tiker_symbol` (string): specific stock ticker symbol (e.g., AAPL for Apple Inc.)
`period` (string): stock data in what period, default value is 3 years 

2. `update_stock_data`

**what it does**: Update all files in the database to include latest stock price information.

3. `get_filtered_stock_data`

**what it does**: Fetch stock data of the ticker within given timeframe from the statistic database.

**inputs**: `ticker_symbol` (string), `start_date` (string, optional), `end_date` (string, optional).

**outputs**: a DataFrame containing the filtered stock data.

**Pseudocode**
```
def get_filtered_stock_data(ticker_symbol, start_date, end_date):
    if isValid(ticker_symbol, start_date, end_date):
        filteredData = df[start_date <= "Date" <= end_date]
        return filteredData
```

### Sub-component 2 Technical Indicators Manager

#### Overview

The Technical Indicators Manager is a core component designed to calculate and display Key Performance Indicators (KPIs) for selected stocks using various technical indicators. It processes user inputs, performs calculations, and outputs the results for visualization, contributing to decision-making processes in financial analysis.

#### Modules
`backend.kpi_manager` and `backend.technical_indicators`

**Input**:
- User selection of a stock from a dropdown menu.
- Selection of a technical indicator (e.g., Moving Average, RSI) from another dropdown menu.
- Input of the length for the selected technical indicator (e.g., 14 days for RSI) through a field box.

**Outputs**:
- Calculated data for the selected technical indicator, formatted for integration with company filter outputs.

**Assumptions**:
- Users have a basic understanding of the selected technical indicators and their implications.

**Pseudocode**:
```
def calculate_rsi(self, data, period):
    # RSI calculation logic
    return rsi_values
```
```
def format_data(self, data, format_type):
    # Formatting data based on the specified type (overlay or  oscillator)
    return formatted_data
```

#### Interaction with Other Components:
- Charts: Utilizes the calculated KPIs to generate various charts, enhancing data visualization with tooltips, labels, axes, and data points.
- Interactivity Filters: Works with filters (date, time, company) to refine the displayed data based on user selections.
- Design and Layout: The output format (e.g., visualization types) is adapted based on the overall design and layout specifications to ensure consistency across the dashboard.
 

### Sub-component 3 Visualization Manager

#### Overview
The visualization manager creates and controls all interactive plots of data price and technical indicators using `plotly` package. 

#### Interaction with Other Components
Interact with Stock Data Manager and Technical Indicator Manager to retrieve data points under plots. Also interact with the UI component to display the plots.

#### Modules
1. `backend.visualization`

#### Key Functions
1. `plot_stock_price`

**Input**: `ticker_symbol` (string)

**output**: a interactive plot object with readable tooltips, labels, time buttons.

2. `plot_kpis`

**Input**: `stock_fig` (Plotly object), `ticker_symbol` (string), `length` (int), `kpi_name` (string)

**Output**: a interactive plot object with readable tooltips, labels, time buttons.

## Component 3 Backend News Data Processor

### Sub-component 1 News Data Downloader

#### Sub-component - `get_news_data`

**what it does**: collect news data specified by company name and timeframe through EODHD news API.

**Input**:

- company name (string): specific stock ticker symbol
- start date (string): start timeframe of news, default value is 2021-01-01
- end date (string): end timeframe of news, default value is 2024-02-01

**Output**:

- json files containing news data for specific companies starting from 3 years ago.
- columns: title, date, content, url

**Pseudocode**:
```
function get_news_data(company, start_date, end_date):

    url = create_api_url(company, start_date, end_date)
    news_data = requests.get(url)
    format_news_data # clean and reformat raw data
    update_database(news_data)
return
```

### Sub-component 2 Sentiment Analysis

#### Overview

The Sentiment Analysis component calculates the sentiments attaced to a particular article title and/or content for a given list of titles associated to a company.

**Input**:

- Does not involve user input but the inputs are part of in process data movement.
- Internally, the selected date range filters the dataset of a specific company's stock and the corresponding price percent change to retrienve a date range and list of news article titles. This list of articles is subsequently passed to the sentiment analysis functions responsible for calculating the sentiment of the titles.

**Output**:

- A dictionary of articels and their corresponding sentiment scores which are then used for filtering and displaying data

**Assumptions**:

- Users have initially selected the company stock they are interested in.
- Their are only 3 sentiments attached to a given string - negative, positive or neutral

**Interaction with Other Components**:

Interacts with Data Manager to retrieve filtered data and Visualization Manager for display:.

**Pseudocode**:
```
function get_sentiment_value(title_list) -> dict:

    analyzer = create_SentimentIntensityAnalyzer() 
    for each sentence in title_list:
        vs = analyze_polarity(analyzer, sentence) 
        senti_dict[sentence] = vs 
    return senti_dict

```

## Interaction to accomplish use case

### Interaction Diagram - Sentiment Analysis
![Sentiment Analysis Diagram](https://github.com/shivam096/dinero/blob/main/docs/images/Interaction_Diagram_2.png)

### Use Case - Sentiment Analysis

**Objective**: System displays sentiment analysis results based on users interest

User: Input time frame and percentage changes in price that they are interested in.

System: Retrieve relevent stock and news data, apply sentiment analysis, and display the results.

**Components Interacted**:

1. User Interface-UI Filter and Input Boxes
2. News Data Proessor - News Data Downloader
3. News Data Proessor - Sentiment Analysis

### Interaction Diagram - KPI Plots
![Sentiment Analysis Diagram](https://github.com/shivam096/dinero/blob/main/docs/images/Interaction_Diagram_1.png)

### Use Case - KPI Plots

**Objective**: System displays KPIs of interest to the user for specific stocks

User: Accesses the main page where the filter by company is selected. User clicks a button for the technical indicator and input length of period of interest.

System: Displays the technical indicator of interest and company stock

**Components Interacted**:

1. User Interface-UI Filter and Input Boxes
2. Stock Data Proessor - Visualization
3. Stock Data Proessor - Technical Indicator Manager
4. Stock Data Proessor - Stock Data Indicator Manager