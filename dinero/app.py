import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import time

from backend.visualization import plot_stock_price
from backend.visualization import plot_kpis

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

    # create vis
    fig_price = plot_stock_price(company_option)
    # Store the initial view as session state
    if 'initial_view' not in st.session_state:
        st.session_state.initial_view = fig_price.to_dict()
 
    st.plotly_chart(fig_price, use_container_width=True)

    # "Return to Initial View" button
    if st.button('Return to Initial View'):
        fig_price.update(st.session_state.initial_view)

    # Filter inputs
    kpi_name = st.selectbox('Select Technical Indicator', ('MA', 'RSI', 'ROC', 'BBP'))
    length = st.number_input('Input a length')

    fig_kpi = plot_kpis(fig_price, company_option, length, kpi_name)
    
    if fig_kpi:
        st.plotly_chart(fig_kpi)
    else:
        st.plotly_chart(fig_price)

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