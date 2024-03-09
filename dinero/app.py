import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from backend.visualization import plot_stock_data, plot_stock_price
from backend.visualization import plot_kpis
from backend.kpi_manager import get_technical_indicator
from backend.app_functions import retrieve_data, streamlit_filtering_by_date

st.set_page_config(layout="wide")

heading_color = "#86B6F6"
title_color = "#DBE7C9"
positive_color = "#527853"  # Green
neutral_color = "#B4B4B8"    # Yellow
negative_color = "#D24545"   # Red

company_stock_mapping = {
    "AAPL" : "APPLE",
    "GOOG" : "GOOGLE",
    "MSFT" : "MICROSOFT",
    "NVDA" : "NVIDIA",
    "TSLA" : "TESLA"
}


st.image("frontend/logo.png", use_column_width=True)

st.sidebar.header("Filters for Data")
company_option = st.sidebar.selectbox('Select one symbol', ('AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA'))

percentage_change_option = st.sidebar.selectbox('Select Percentage Change in Stock Price', ('10%', '5%', '-5%', '-10%'))

tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])

with tab1:
    st.markdown("<h2 style='color:{}; text-align: center;'>{} STOCK PERFORMANCE VISUALIZATION</h2>".format(heading_color, company_stock_mapping[company_option]), unsafe_allow_html=True)
    # create vis
    fig_price = plot_stock_price(company_option)

    # Store the initial view as session state
    if 'initial_view' not in st.session_state:
        st.session_state.initial_view = fig_price.to_dict()

    st.plotly_chart(fig_price, use_container_width=True)

    # "Return to Initial View" button
    if st.button('Return to Initial View'):
        fig_price.update(st.session_state.initial_view)

    # Initialize empty DataFrame (optional)
    if 'stock_data' not in st.session_state:
        st.session_state['stock_data'] = pd.DataFrame()

    # Filter inputs
    st.markdown("<h2 style='color:{}; text-align: center;'>LEVERAGING TECHNICAL INDICATORS</h2>".format(heading_color), unsafe_allow_html=True)
    kpi_name = st.selectbox('Select Technical Indicator', ('MA', 'RSI', 'ROC', 'BBP'))
    tooltip_text = "This is where you input the length."

    length = st.number_input('Input a length')

    fig_kpi = plot_kpis(fig_price, company_option, length, kpi_name)
    #st.plotly_chart(fig_kpi, use_container_width=True)

    if fig_kpi:
        st.plotly_chart(fig_kpi, use_container_width=True)
    else:
        st.plotly_chart(fig_price, use_container_width=True)


with tab2:
    st.markdown("<h2 style='color:{}; text-align: center;'>BEYOND HEADLINES : DECODING NEWS SENTIMENT</h2>".format(heading_color), unsafe_allow_html=True)
    with st.expander(f"**Headline**"):
        st.write("This is the News Article (if relevant)")

    # Display the metrics in a single row

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h1 style='color:{}; text-align: center;'>0.70</h1>".format(positive_color), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Positive Sentiment Score 😄</p>", unsafe_allow_html=True)

    # Metric 2: Neutral Sentiment Score
    with col2:
        st.markdown("<h1 style='color:{}; text-align: center;'>0.50</h1>".format(neutral_color), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Neutral Sentiment Score 😐</p>", unsafe_allow_html=True)

    # Metric 3: Negative Sentiment Score
    with col3:
        st.markdown("<h1 style='color:{}; text-align: center;'>0.23</h1>".format(negative_color), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Negative Sentiment Score ☹️</p>", unsafe_allow_html=True)