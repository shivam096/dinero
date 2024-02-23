import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.header("DINERO - Analyze Stocks and Market Sentiment")
#st.image("frontend/favicon.png", width=100)

st.sidebar.header("Filters for Data")
company_option = st.sidebar.selectbox('Select one symbol', ('AAPL', 'GOOG', 'MSFT'))

def retrieve_data(company_option):
    file_path = f'data/{company_option}.csv' 
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.reset_index(inplace=True)
    return df

def streamlit_filtering_by_date(df):
    
    default_start_date = df['Date'].iloc[0]
    default_end_date = df['Date'].iloc[-1]
 
    start_date = st.sidebar.date_input('Start date', default_start_date )
    end_date = st.sidebar.date_input('End date', default_end_date )
    # Convert Python date objects to Pandas datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if start_date < end_date:
        st.sidebar.success(f'Start date: `{start_date}`\n\nEnd date:`{end_date}`')
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df.reset_index(inplace=True)
    return df


df = retrieve_data(company_option)
df = streamlit_filtering_by_date(df)
progress_bar = st.progress(0)

percentage_change_option = st.sidebar.selectbox('Select Percentage Change in Stock Price', ('10%', '5%', '-5%', '10%'))

tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])


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
    
    st.selectbox('Select Technical Indicator', ('RSI', 'MACD'))
    length = st.number_input('Input a length')

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


with tab2:
    st.header("News Headlines and Articles")
    with st.expander("Headline"):
        st.write("This is the News Article (if relevant)")
        
    # Define the colors for the "value" fields
    positive_color = "#00cc00"  # Green
    neutral_color = "#ffcc00"    # Yellow
    negative_color = "#ff3300"   # Red

    # Display the metrics in a single row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Positive Sentiment Score", value="0.70")

    # Metric 2: Neutral Sentiment Score
    with col2:
        st.metric(label="Neutral Sentiment Score", value="0.50")

    # Metric 3: Negative Sentiment Score
    with col3:
        st.metric(label="Negative Sentiment Score", value="0.20")