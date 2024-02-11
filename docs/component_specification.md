# Component Specification. 

## Software components. 

High level description of the software components such as: data manager, which provides a simplified interface to your data and provides application specific features (e.g., querying data subsets); and visualization manager, which displays data frames as a plot. Describe at least 3 components specifying: what it does, inputs it requires, and outputs it provides. If you have more significant components in your system, we highly suggest documenting those as well.

### Data Manager

- The purpouse of this component is to extract stock and news data from Yahoo Finance and process the raw data into the format required by the rest of the project.

- sub-component: stock data

what it does: extract stock data specified by company name and time through yfinance API call.

input: company name (string), time period (string)

- sub-component: news data

what it does: extract news data specified by company name and time through yfinance API call.

input: company name (string), time period (string)

- Workflow:
- 1. Extract data through yfinance API call.
- 2. Clean data by dropping irrelevent columns.
- 3. Save the data file.

## Interactions to accomplish use cases. 
Describe how the above software components interact to accomplish your use cases. Include at least one interaction diagram.