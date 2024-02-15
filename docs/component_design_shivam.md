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

### Component 2 : Sentiment Analysis 
**Overview**
The Sentiment Analysis component calculates the sentiments attaced to a particular article title and/or content for a given list of titles associated to a company.

**Input**
- Does not involve user input but the inputs are part of in process data movement.
- Internally, the selected date range filters the dataset of a specific company's stock and the corresponding price percent change to retrienve a date range and list of news article titles. This list of articles is subsequently passed to the sentiment analysis functions responsible for calculating the sentiment of the titles.

**Output**
- A dictionary of articels and their corresponding sentiment scores which are then used for filtering and displaying data

**Assumptions**
- Users have initially selected the company stock they are interested in.
- Their are only 3 sentiments attached to a given string - negative, positive or neutral

**Interaction with Other Components**
Interacts with backend functions to retrieve filtered data for visualization and display:
1. Function for displaying news headlines and articles.

**Pseudocode**
```
function get_sentiment_value(title_list) -> dict:

    analyzer = create_SentimentIntensityAnalyzer() 
    for each sentence in title_list:
        vs = analyze_polarity(analyzer, sentence) 
        senti_dict[sentence] = vs 
    return senti_dict

```