# All imports
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly.graph_objects as go

st.header("DINERO")

# Sidebar for all data filters - 
# Currently has - Company filter
#                 Date Filter 
# Also will have - Sentiment Tag
#                 Keywords


# Company Filter (drop down)
option = st.sidebar.selectbox('Select one symbol', ('AAPL', 'MSFT'))

# Date filter - Calander 
today = datetime.date.today()
before = today - datetime.timedelta(days=700)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')
    
    
tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])


# Retrieving data - will be changed
df = yf.download(option, start=start_date, end=end_date, progress=False)

# Reset index to get the 'Date' column
df.reset_index(inplace=True)

# Function to generate dummy news headlines and events
def generate_dummy_news(company, start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    headlines = [f"{company} announces new product", f"{company} reports earnings", f"{company} CEO interviewed"]
    events = ["Product launch", "Earnings release", "CEO interview"]
    np.random.seed(0)
    news_data = {
        "Date": np.random.choice(dates, size=10),
        "Headline": np.random.choice(headlines, size=10),
        "Event": np.random.choice(events, size=10)
    }
    return pd.DataFrame(news_data)

dummy_news_df = generate_dummy_news(option, start_date, end_date)
dummy_news_df.reset_index(inplace=True)

with tab1:
    st.header("Stock Visualizations and Technical Indicators")
    # Plotly plot for stock data 
    # Create a figure for line chart
    fig_line = go.Figure()

    # Add trace for stock prices
    fig_line.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))

    buttons = []
    for i in range(len(df)):
        date = df['Date'][i]
        close_price = df['Close'][i]
        button = dict(label=str(date), method='update', args=[{'x': [[date]], 'y': [[close_price]]}])
        buttons.append(button)

    # Add buttons to layout
    fig_line.update_layout(updatemenus=[{'buttons': buttons,
                                    'direction': 'down',
                                    'showactive': True,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'y': 1.15,
                                    'yanchor': 'top'}],
                    title="Stock Prices Over Time",
                    xaxis_title="Date", yaxis_title="Price")

    # Add tooltip
    fig_line.update_traces(hovertemplate="Date: %{x}<br>Close Price: %{y}")

    # Show line chart
    st.plotly_chart(fig_line)

    # Create a figure for candlestick chart - Demo/Trial
    fig_candlestick = go.Figure()

    # Add trace for candlestick chart
    fig_candlestick.add_trace(go.Candlestick(x=df['Date'],
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'],
                                            name='Candlestick'))

    # Update layout for candlestick chart
    fig_candlestick.update_layout(title="Candlestick Chart",
                                xaxis_title="Date", yaxis_title="Price")

    # Show candlestick chart
    st.plotly_chart(fig_candlestick)

    progress_bar = st.progress(0)


with tab2:
    st.header(st.markdown("# News Headlines and Articles"))
    with st.expander("Headline"):
        st.write("This is the News Article (if relevant)")
