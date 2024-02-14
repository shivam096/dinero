# Component Specification. 

## KPI Manager Component

**Overview**
The KPI Manager is a core component designed to calculate and display Key Performance Indicators (KPIs) for selected stocks using various technical indicators. It processes user inputs, performs calculations, and outputs the results for visualization, contributing to decision-making processes in financial analysis.

**Input**

- User selection of a stock from a dropdown menu.
- Selection of a technical indicator (e.g., Moving Average, RSI) from another dropdown menu.
- Input of the length for the selected technical indicator (e.g., 14 days for RSI) through a field box.

**Outputs**

- Calculated data for the selected technical indicator, formatted for integration with company filter outputs.
- Visual representations of the KPIs, such as line graphs or pie charts, depending on the selected KPI metric.

**Assumptions**

- The list of available stocks and technical indicators is accurate and up-to-date.
- Users have a basic understanding of the selected technical indicators and their implications.

**Interaction with Other Components**

- Charts: Utilizes the calculated KPIs to generate various charts, enhancing data visualization with tooltips, labels, axes, and data points.
- Interactivity Filters: Works with filters (date, time, company) to refine the displayed data based on user selections.
- Design and Layout: The output format (e.g., visualization types) is adapted based on the overall design and layout specifications to ensure consistency across the dashboard.
 
### Pseudocode

**Data Fetcher Component**
1. This component abstracts the data acquisition layer from the calculation logic, making it easier to update data sources or fetching strategies without affecting the rest of the system.
```
def fetch_stock_data(self, symbol):
    # fetching of stock data
    return data
```
**Indicator Calculator Component**
2. Focuses on calculating various technical indicators.

```
def calculate_rsi(self, data, period):
    # RSI calculation logic
    return rsi_values
```
**Input Handler Component**
3. Manages input from the front end, validating and parsing it before it's processed.
```
def handle_input(self, input_data):
    # Validating and parsing input data
    return validated_data
```

**Output Formatter Component**
4. Formatting the calculated data into a structure suitable for front-end display.
```
def format_data(self, data, format_type):
    # Formatting data based on the specified type (overlay or  oscillator)
    return formatted_data
```