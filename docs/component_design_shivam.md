## Software Components 

### Component 4 : Displaying Event Data (Title and Content)
**Overview**
The Event Data (Title and Content) component displays news articles and its titles specific to a chosen company.

**Input**
- User selects a company from a predefined dropdown menu on the user interface and a percent change filter
- Internally, the input is a list of dates containing the dates on which the percent change was greater or lower based on the selected filter. This string is passed to a news API functions responsible for fetching content and title and displaying data.

**Output**
- Display of news headlines and articles relevant to the selected company.

**Assumptions**
- The changes that the user can apply can apnly be 5% or 10%
- Users are familiar with the companies available in the dropdown menu.

**Interaction with Other Components**
Interacts with sentiment analysis component to retrieve sentiment value for displaying data.
1. Function for displaying news headlines and articles.

**Pseudocode**
```
function getDatesforarticles(selectedCompany, percentchange):
    dates_for_articles = find_count_value_change

    for date in dates_for_articles:
        api_response = get_news_articles()
        filtered_articles # filter articles for the specific company only
        news_articles_links[date] = filtered_articles

    return news_articles_links
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