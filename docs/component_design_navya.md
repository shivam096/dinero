## Software Components to Facilitate Interactivity

### Component 1 : Company Filter
**Overview**
The Company Filter component facilitates user interaction to display graphs, technical indicators, and news articles specific to a chosen company.

**Input**
- User selects a company from a predefined dropdown menu on the user interface.
- Internally, the input is a string representing the selected company from a pre-defined list. This string is passed to various functions responsible for generating visualizations and displaying data.

**Output**
- Plotly line charts illustrating stock trends.
- Plotly charts representing various technical indicators.
- Display of news headlines and articles relevant to the selected company.
- Internally, data is filtered to include information specific to the chosen company before being processed and displayed.

**Assumptions**
- The dropdown menu contains an accurate and pre-defined list of companies.
- Users are familiar with the companies available in the dropdown menu.

**Interaction with Other Components**
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

### Component 2 : Date Filter
**Overview**
The Date Filter component allows users to select a specific date range for viewing or analyzing the stock of a particular company.

**Input**
- Users select a start date and end date from a calendar dropdown menu on the user interface.
- Internally, the selected date range filters the dataset of a specific company's stock. These two date parameters are subsequently passed to various functions responsible for data visualization and display.

**Output**
- Plotly line charts illustrating stock trends.
- Plotly charts representing various technical indicators.
- Display of news headlines and articles relevant to the selected company within the specified date range.
- Internally, data is filtered to include information specific to the date range for the chosen company before being processed and displayed.

**Assumptions**
- Users have initially selected the company stock they are interested in.
- The calendar dropdown menu contains dates that fall within the available date ranges in the dataset. If an invalid date is selected, an error will be thrown, prompting the user to choose again.
- The start date must precede the end date. If this condition is not met, an error will be thrown, and the user will be prompted to choose again.

**Interaction with Other Components**
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
### Component 3 : Button on Plotly Line Graph
**Overview**
The Button on the Line Graph component represents the stock trends of a specified company within a specified date range. These buttons appear when there is a significant increase or decrease in the stock value, typically at thresholds such as 5% or 10%. Upon clicking these buttons, users are redirected to a new tab displaying a headline or an article corresponding to the drastic change that occurred.

**Input**
- Users interact with these buttons by clicking on them to view news headlines or articles related to the drastic stock price changes.
- The input for this component is generated dynamically based on predefined events of significant stock price changes.
- These events trigger the appearance of buttons on the plotly line graph.

**Output**
- Redirection to news headlines or articles corresponding to the drastic change in the stock price of a specific company within a specific date range.

**Assumptions**
- There exists a static dataset containing predefined events of significant stock price changes.
- Buttons are displayed only for the relevant news headlines and articles corresponding to these events.
- Users understand that the buttons are associated with significant stock price changes.
- The news articles or headlines are storedis accessible when redirected upon button click.

**Pseudocode**
```
def buttonsOnGraph(data):
    significantEvents = findSignificantEvents(data)

    # Function to display a button on the plotly line graph for a significant increase or decrease in stock price
    # Button redirects to a news article or headline corresponding to the increase or decrease

```

## Software Components for Design and Layout using `streamlit` Python Package

### Component 1 : Steamlit Tab Component

**Overview**
The Streamlit Tab Component facilitates the organization of different information into separate tabs on the Streamlit frontend. In our application, we have planned to utilize two tabs: one for displaying Plotly line graphs depicting stock trends and technical indicators, and the other for presenting relevant news articles based on sentiment analysis. 

**Usage**
- The tab functionality enables users to easily switch between different categories of information. 
- Each tab can contain distinct sets of components and functionality tailored to its specific purpose.

**Sample Code**
```
tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])

with tab1:
    # Remaining code for Tab 1

with tab2:
    # Remaining code for Tab 2
```

### Component 2 : Streamlit Expander Component
The Streamlit Expander Component allows for the collapsible display of additional content within a section. In our application, we intend to use the expander to present news headlines initially, and upon user interaction, expand to reveal further details such as the full news article, publication date, and source.

**Usage**
- Users can expand or collapse the content within the expander section using a toggle button.
- The expander component helps to maintain a clean and organized layout by initially displaying only essential information, with the option to reveal additional details as needed.

**Sample Code**
```
with st.expander("News Headline"):
    st.write("News Article")
```