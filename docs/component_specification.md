# Component Specification

## Software Components

### Component 1. Data Manager

#### Overview

The Data Manager component is designed to build the static datasets by extracting stock data from Yahoo Finance and news data through EODHD API calls. Besides, it provides access to cleaned data formatted as required by other components of the project. 

#### Interaction with Other Components

Interacts with all other components. Only called by backend functions to retrieve subset of data from static database.


#### Sub-component - `get_stock_data`

**what it does**: collect stock data specified by company name and time through yfinance API call.

**Input**:

- company name (string): specific stock ticker symbol (e.g., AAPL for Apple Inc.)
- period (string): stock data in what period, default value is 3 years

**Output**:

- csv files containing 3 years, unless otherwise specified, of stock information for companies: Microsoft, Google, Apple
- columns: Open, High, Low, Close, Adj Close, Volume

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

#### Sub-component - `get_dataset`

**what it does**: access to the database (stored in google drive)

**Input**:

- company name (string): specific stock ticker symbol
- data type (string): stock or news
- start date (string): start timeframe
- end date (string): end timeframe

**Output**

- subset of data as required (pandas dataframe)

### Component 2. Visualization Manager

#### Overview

The visualization manager creates and controls all visualizations. 

#### Sub-component - `create_plot`

**what it does**: create different plots from input dataframe.

**Input**: dataframe (stock data / KPIs)

**output**: 

- charts / line graph based on the input type
- set readable tooltips, labels, axes

#### Sub-component - `display_events`

**what it does**: displays news articles and their titles specific to a chosen company.

**Input**:

- selectedCompany (string)
- percentchange (float)
- Internally, the input is a list of dates containing the dates on which the percent change was greater or lower based on the selected filter. This string is passed to a news API functions responsible for fetching content and title and displaying data.

**Output**:

- Display of news headlines and articles relevant to the selected company.

**Assumptions**:

- User selects a company from a predefined dropdown menu on the user interface and a percent change filter.
- Users are familiar with the companies available in the dropdown menu.
- The changes that the user can apply can apnly be 5% or 10%.

**Interaction with Other Components**:
Interacts with sentiment analysis component to retrieve sentiment value for displaying data.

**Pseudocode**:

```
function getDatesforarticles(selectedCompany, percentchange):
    dates_for_articles = find_count_value_change

    for date in dates_for_articles:
        api_response = get_news_articles()
        filtered_articles # filter articles for the specific company only
        news_articles_links[date] = filtered_articles

    return news_articles_links
```

#### Sub-component - `buttonsOnGraph`

**what it does**:  add buttons when there is a significant increase or decrease in the stock value, typically at thresholds such as 5% or 10%. These buttons represent the stock trends of a specified company within a specified date range. Upon clicking these buttons, users are redirected to a new tab displaying a headline or an article corresponding to the drastic change that occurred.

**Input**:

- The input for this component is generated dynamically based on predefined events of significant stock price changes.
- These events trigger the appearance of buttons on the plotly line graph.

**Output**:

- Redirection to news headlines or articles corresponding to the drastic change in the stock price of a specific company within a specific date range.

**Assumptions**:

- There exists a static dataset containing predefined events of significant stock price changes.
- Buttons are displayed only for the relevant news headlines and articles corresponding to these events.
- Users understand that the buttons are associated with significant stock price changes.
- Users interact with these buttons by clicking on them.
- The news articles or headlines are storedis accessible when redirected upon button click.

**Pseudocode**:

```
def buttonsOnGraph(data):
    significantEvents = findSignificantEvents(data)

    # Function to display a button on the plotly line graph for a significant increase or decrease in stock price
    # Button redirects to a news article or headline corresponding to the increase or decrease

```
### Component 3. Design and Layout 

#### Overview
The Design and Layout component creates interactive web applications and builds intuitive and visually appealing user interfaces using `streamlit` Python Package.

#### Sub_component - Steamlit Tab

**what it does**:

The Streamlit Tab Component facilitates the organization of different information into separate tabs on the Streamlit frontend. In our application, we have planned to utilize two tabs: one for displaying Plotly line graphs depicting stock trends and technical indicators, and the other for presenting relevant news articles based on sentiment analysis. 

**Usage**:

- The tab functionality enables users to easily switch between different categories of information. 
- Each tab can contain distinct sets of components and functionality tailored to its specific purpose.

**Sample Code**:

```
tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])

with tab1:
    # Remaining code for Tab 1

with tab2:
    # Remaining code for Tab 2
```

#### Sub_component - Streamlit Expander

**what it does**:

The Streamlit Expander Component allows for the collapsible display of additional content within a section. In our application, we intend to use the expander to present news headlines initially, and upon user interaction, expand to reveal further details such as the full news article, publication date, and source.

**Usage**:

- Users can expand or collapse the content within the expander section using a toggle button.
- The expander component helps to maintain a clean and organized layout by initially displaying only essential information, with the option to reveal additional details as needed.

**Sample Code**:

```
with st.expander("News Headline"):
    st.write("News Article")
```

### Component 4. Interactivity

#### Overview

The Interactivity implements interactivity to the graphs and web applications.

#### Sub-component - Company Filter

**what it does**:

The Company Filter component facilitates user interaction to display graphs, technical indicators, and news articles specific to a chosen company.

**Input**:

- User selects a company from a predefined dropdown menu on the user interface.
- Internally, the input is a string representing the selected company from a pre-defined list. This string is passed to various functions responsible for generating visualizations and displaying data.

**Output**:

- data filtered to include information specific to the chosen company.
- Internally, recreate visualizations by interacting with the Visualization Manager.

**Assumptions**:

- The dropdown menu contains an accurate and pre-defined list of companies.
- Users are familiar with the companies available in the dropdown menu.

**Interaction with Other Components**:

Interacts with backend functions to retrieve filtered data for visualization and display:
1. Plotly function for visualizing the line graph of stock trends.
2. Plotly function for visualizing various technical indicators.
3. Function for displaying news headlines and articles.

**Pseudocode**
```
def filterCompany(selectedCompany):
    if isValidCompany(selectedCompany):
        filteredData = df[df["Company"] == selectedCompany]
        return filteredData
```

#### Sub-component - Date Filter

**what it does**:

The Date Filter component allows users to select a specific date range for viewing or analyzing the stock of a particular company.

**Input**:

- Users select a start date and end date from a calendar dropdown menu on the user interface.
- Internally, the selected date range filters the dataset of a specific company's stock. These two date parameters are subsequently passed to various functions responsible for data visualization and display.

**Output**:

- data filtered to include information specific to the date range for the chosen company.
- Internally, recreate visualizations by interacting with the Visualization Manager.

**Assumptions**:

- Users have initially selected the company stock they are interested in.
- The calendar dropdown menu contains dates that fall within the available date ranges in the dataset. If an invalid date is selected, an error will be thrown, prompting the user to choose again.
- The start date must precede the end date. If this condition is not met, an error will be thrown, and the user will be prompted to choose again.

**Interaction with Other Components**:

Interacts with backend functions to retrieve filtered data for visualization and display:
1. Plotly function for visualizing the line graph of stock trends.
2. Plotly function for visualizing various technical indicators.
3. Function for displaying news headlines and articles.

**Pseudocode**
```
def filterDate(startDate, endDate):
    if isValidDate(startDate, endDate):
        filteredData = getDataWithinDateRange(startDate, endDate)
        return filteredData

def isValidDate(startDate, endDate):
    # Check if date range is valid for the given dataset
    # startDate < endDate
    if startDate < endDate:
        return True
    else:
        return False
```

### Component 4. KPI Manager Component

#### Overview

The KPI Manager is a core component designed to calculate and display Key Performance Indicators (KPIs) for selected stocks using various technical indicators. It processes user inputs, performs calculations, and outputs the results for visualization, contributing to decision-making processes in financial analysis.

**Input**:

- User selection of a stock from a dropdown menu.
- Selection of a technical indicator (e.g., Moving Average, RSI) from another dropdown menu.
- Input of the length for the selected technical indicator (e.g., 14 days for RSI) through a field box.

**Outputs**:

- Calculated data for the selected technical indicator, formatted for integration with company filter outputs.
- Visual representations of the KPIs, such as line graphs or pie charts, depending on the selected KPI metric.

**Assumptions**:

- The list of available stocks and technical indicators is accurate and up-to-date.
- Users have a basic understanding of the selected technical indicators and their implications.

#### Sub-component - Data Fetcher

**what it does**:
This component abstracts the data acquisition layer from the calculation logic, making it easier to update data sources or fetching strategies without affecting the rest of the system.

**Pseudocode**:
```
def fetch_stock_data(self, symbol):
    # fetching of stock data
    return data
```

#### Sub-component - Indicator Calculator

**what it does**:
Focuses on calculating various technical indicators.

**Pseudocode**:
```
def calculate_rsi(self, data, period):
    # RSI calculation logic
    return rsi_values
```

#### Sub-component - Input Handler

**what it does**:
Manages input from the front end, validating and parsing it before it's processed.

**Pseudocode**:
```
def handle_input(self, input_data):
    # Validating and parsing input data
    return validated_data
```

#### Sub-component - Output Formatter

**what it does**:
Formatting the calculated data into a structure suitable for front-end display.

**Pseudocode**:
```
def format_data(self, data, format_type):
    # Formatting data based on the specified type (overlay or  oscillator)
    return formatted_data
```

#### Interaction with Other Components:

- Charts: Utilizes the calculated KPIs to generate various charts, enhancing data visualization with tooltips, labels, axes, and data points.
- Interactivity Filters: Works with filters (date, time, company) to refine the displayed data based on user selections.
- Design and Layout: The output format (e.g., visualization types) is adapted based on the overall design and layout specifications to ensure consistency across the dashboard.
 
### Component 5. Sentiment Analysis 

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

### System Interaction Diagram
![System_design](https://github.com/shivam096/dinero/blob/main/docs/System_design.jpg)

### Interaction Diagram - Sentiment Analysis
![Sentiment Analysis Diagram](https://github.com/shivam096/dinero/blob/main/docs/Sentiment%20Analysis%20Diagram.jpeg)

### Use Case - Sentiment Analysis

**Objective**: System displays sentiment analysis results based on users interest

User: Select company name and time frame that they are interested in.

System: Retrieve relevent stock and news data, apply sentiment analysis, and display the results.

**Components Interacted**:

1. Interactivity
2. Data Manager
3. Sentiment Analysis
4. Design and Layout



