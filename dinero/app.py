"""
Module level docstring for Stock Dashboard Application

This module contains the main functionality for a Stock
Dashboard Application.The application is built using Streamlit
and provides various features including:

    1. Stock Performance Overview: Allows users to visualize
        the stock performance of selected companies.
    2. Explore Stock Technical Indicators: Provides insights into
        technical indicators such as Moving Average, RSI, ROC, and BBP.
    3. Latest News Headlines and Articles: Displays news headlines
        related to selected stocks and their sentiment analysis.
    4. Explore More Tickers or Update Data: Allows users to add
        new tickers and update stock data.

This module imports necessary functions and classes from backend
modules for data processing, visualization, and sentiment analysis.

Example Usage:
    $ streamlit run app.py

"""
import streamlit as st
import pandas as pd

from backend.visualization import plot_stock_price
from backend.visualization import plot_kpis
from backend.stock_data_manager import (
    download_stock_data,
    update_stock_data,
    get_existing_tickers,
    get_last_n_days
)
from backend.processing import get_sentiments



st.set_page_config(layout="wide")

HEADING_COLOR = "#86B6F6"
NEWS_ARTICLE_COLOR = "#E3DFFD"
NEWS_ARTICLE_DATE_COLOR = "#89CFF3"
TITLE_COLOR = "#DBE7C9"
POSITIVE_COLOR = "#527853"  # Green
NEUTRAL_COLOR = "#B4B4B8"    # Yellow
NEGATIVE_COLOR = "#D24545"   # Red
HIGHLIGHT_COLOR_BLUE = "#AEDEFC"

kpi_description_mapping = {
    "MA" : f'''The <span style='color:{NEGATIVE_COLOR}'><b>Moving Average (MA)
            </b></span> helps <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>smooth out
            short-term price fluctuations</i></span> to reveal the underlying
            trend. Imagine calculating the average price of a stock over a
            set period (like 20 days or 50 days). This helps
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>visualize the general
            direction (upward, downward, or sideways)</i></span>
            and spot trends to figure out when the stock might change direction.''',
    "RSI": f'''<span style='color:{NEGATIVE_COLOR}'><b>Relative Strength Index (RSI)
            </b></span> is like a speedometer for stocks! It tells us
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>how fast the price of a
            stock is changing.</i></span> When RSI is
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>high</i></span>, it means
            the stock might be <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>going up
            too fast and could slow down.</i></span> When RSI is
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>low</i></span>, it means the stock
            might be <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>going down too fast and
            could bounce back up.</i></span>''',
    "ROC": f'''<span style='color:{NEGATIVE_COLOR}'><b>Rate of Change (ROC)</b></span>
            tells you <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>how much the price
            has changed over a certain period of time,</i></span> expressed as a percentage.
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>Positive ROC</i></span> means the
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>price is going up,</i></span>
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>negative ROC</i></span> means
            it's <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>going down.</i></span>
                It helps you understand <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>how
                quickly the price is moving in one direction or another.</i></span>''',
    "BBP": f'''<span style='color:{NEGATIVE_COLOR}'><b>Bollinger Bands Percentage
            (BBP)</b></span> is like a rubber band around a stock's price!
            These bands are a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>volatility
            indicator </i></span>, with a <span style='color:{HIGHLIGHT_COLOR_BLUE}'>
            <i>wider band signifying higher volatility</i></span> and a
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>narrower band indicating
            lower volatility.</i></span> BBP values close to 0 suggest the price
            is near the lower band, potentially <span style='color:
            {HIGHLIGHT_COLOR_BLUE}'><i> hinting at oversold conditions</i></span>.
            Conversely, values close to 100 indicate the price is near the upper
            band, potentially <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>
            suggesting overbought conditions.</i></span>'''
}

kpi_chart_info_mapping = {
"MA": f'''When a stock price increeases above the <span style='color:{NEGATIVE_COLOR}'>
        <b>moving average</b></span> line it can signal an
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>upward trend</i></span> and a
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>potential buying opportunity.
        </i></span> Conversely, if the <span style='color:{HIGHLIGHT_COLOR_BLUE}'>
        <i>stock price falls below a moving average,</i></span> it might
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>indicate a downtrend</i>
        </span> and a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>potential
        selling point.</i></span> The slope of the moving average
        can also provide insight into the <span style='color:
        {HIGHLIGHT_COLOR_BLUE}'><i> market's direction.</i></span>''',
"RSI": f'''An <span style='color:{NEGATIVE_COLOR}'>b>RSI </b></span>
        value <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>above 70</i></span> indicates
        that a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>stock may be overbought,</i>
        </span> suggesting a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>potential sell
        signal,</i></span> while a value <span style='color:{HIGHLIGHT_COLOR_BLUE}'>
        <i>below 30</i></span> might indicate that a <span style='color:
        {HIGHLIGHT_COLOR_BLUE}'><i>stock is oversold,</i></span> pointing to a
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>potential buy signal.</i>
        </span> Values <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>in between can
        suggest a market in <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>equilibrium,
        </i></span> with <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>no clear
        overbought or oversold signals.</i></span>''',
"ROC": f'''A <span style='color:{NEGATIVE_COLOR}'><b>ROC </b></span>value
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>above zero</i></span>
        suggests an <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>upward
        momentum,</i></span> potentially indicating a <span style='color:
        {HIGHLIGHT_COLOR_BLUE}'><i>buying opportunity,</i></span> while a value
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>below zero can indicate
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i> downward momentum,</i>
        </span> suggesting a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>
        selling or short-selling opportunity.</i></span> The farther the ROC
        moves from zero, the stronger the indicated momentum.''',
"BBP" : f'''A <span style='color:{NEGATIVE_COLOR}'><b>BBP</b></span> value
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>above 1</i></span> indicates a
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>price exceeding the upper
        Bollinger Band, </i></span> which could signal an <span style='color:
        {HIGHLIGHT_COLOR_BLUE}'><i>overbought condition,</i></span> while a value
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>below 0</i></span> indicates
        a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>price below the lower
        band,</i></span> potentially signaling an <span style='color:
        {HIGHLIGHT_COLOR_BLUE}'><i> oversold condition.</i></span>
        Values <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>close to
        0.5</i></span> suggest the price is near the middle band, indicating a
        <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i> lack of strong trend.</i></span>'''
}

st.image("frontend/logo.png", use_column_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["📈 Stock Performance Overview",
                                  "🔍 Explore Stock Technical Indicators",
                                  "📰 Latest News Headlines and Articles",
                                  "💡 Explore More Tickers or Update Data!"])

with tab1:

    company_option = st.selectbox('Choose the Company Stock you Wish to View!',
                                  set(get_existing_tickers()))
    st.markdown(f'''<h2 style='color:{HEADING_COLOR}; text-align: center;'>
                {company_option} : STOCK PERFORMANCE VISUALIZATION</h2>''',
                unsafe_allow_html=True)

    fig_price = plot_stock_price(company_option)

    # Store the initial view as session state
    if 'initial_view' not in st.session_state:
        st.session_state.initial_view = fig_price.to_dict()

    st.plotly_chart(fig_price, use_container_width=True)

    # "Return to Initial View" button
    if st.button('Return to Initial View'):
        fig_price.update(st.session_state.initial_view)

    with st.expander("🛈 How to Read a Candlestick Chart?"):
        st.markdown(f'''
            Each candlestick represents a <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>specific time period</i></span>
            (e.g., one day), displaying four key prices:
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>the opening price, the closing price, the highest
            price (high), and the lowest price (low).</i></span>
            The body of the candlestick, typically <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>colored
            differently for positive and negative price movements,</i></span>
            illustrates the <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>difference between
            the opening and closing prices.</i></span> If the
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>closing
            price is higher than the opening price, the
            candlestick is colored green, indicating a
            price increase,</i></span> while a
            <span style='color:{HIGHLIGHT_COLOR_BLUE}'><i>
            red candlestick signifies a price decrease.</i></span>
            The thin lines above and below the body, called shadows or
            wicks, represent the range between the highest
            and lowest prices during the period.
            Understanding candlestick patterns and
            their formations can provide insights into
            market sentiment and potential future price
            movements.
        ''', unsafe_allow_html=True)


with tab2:
    st.markdown(f'''<h2 style='color:{HEADING_COLOR}; text-align: center;'>
                LEVERAGING TECHNICAL INDICATORS</h2>''', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        kpi_name = st.selectbox('Select Technical Indicator', ('MA', 'RSI', 'ROC', 'BBP'))
        with st.expander(f"🛈 More about {kpi_name}"):
            st.markdown(kpi_description_mapping[kpi_name], unsafe_allow_html=True)

    with col2:
        length = st.number_input('Input a length', value=100, format='%d')

        with st.expander("🛈 What is length?"):
            st.markdown(f'''<span style='color:{NEGATIVE_COLOR}'><b>Length</b></span>
                            typically refers to the <span style='color:{HIGHLIGHT_COLOR_BLUE}'>
                            <b>number of days</b></span> over which the KPI is
                            calculated.''', unsafe_allow_html=True)


    fig_kpi = plot_kpis(fig_price, company_option, length, kpi_name)

    if fig_kpi:
        st.plotly_chart(fig_kpi, use_container_width=True)
    else:
        st.plotly_chart(fig_price, use_container_width=True)

    with st.expander("🛈 What do These Numbers Mean?"):
        st.markdown(kpi_chart_info_mapping[kpi_name], unsafe_allow_html=True)

with tab3:
    st.markdown(f'''<h2 style='color:{HEADING_COLOR}; text-align:
                center;'>BEYOND HEADLINES : DECODING NEWS SENTIMENT</h2>''', unsafe_allow_html=True)
    st.markdown(f'''<h5 style='color:{TITLE_COLOR}';>News Pertaining to {company_option} Stocks</h5>''', unsafe_allow_html=True)

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        number_of_days = st.number_input('''Select News Date Range 📅
                                         (eg. 30 days, 60 days)''', value=90, format='%d')

    with input_col2:
        percentage_change_option = st.number_input('''Choose Stock Price Change
                                                   % 📈''', value=5, format='%d')

    df = get_sentiments(company_option, percentage_change_option)
    df = get_last_n_days(df,number_of_days)
    df['Date'] = pd.to_datetime(df['Date'])
    # df.reset_index(inplace=True)

    col1, col2, col3 = st.columns(3)
    if df.empty:
        st.write(f'''<h5 style='color:{TITLE_COLOR}; text-align: center;'>
                 Oops! 😔 We couldn't find any headlines matching your
                 selected filters.</h5>''', unsafe_allow_html=True)
        st.write(f'''<h5 style='color:{TITLE_COLOR}; text-align: center;'>📰
                 Try adjusting the date range or changing the percentage change
                 in prices to discover more news stories! 💡</h5>''',unsafe_allow_html=True)
    else:
        with col1:
            average_positive_score = round(df['Positive Sentiment Score'].mean(),2)
            average_negative_score = round(df['Negative Sentiment Score'].mean(),2)
            average_neutral_score = round(df['Neutral Sentiment Score'].mean(),2)

            st.markdown(f'''<h1 style='color:{POSITIVE_COLOR}; text-align:
                        center;'>{average_positive_score}</h1>''', unsafe_allow_html=True)
            st.markdown('''<p style='text-align: center;'>Positive
                        Sentiment Score 😄</p>''', unsafe_allow_html=True)

        # Metric 2: Neutral Sentiment Score
        with col2:
            st.markdown(f'''<h1 style='color:{NEUTRAL_COLOR};
                        text-align: center;'>{average_neutral_score}</h1>''',
                        unsafe_allow_html=True)
            st.markdown('''<p style='text-align: center;'>Neutral Sentiment Score 😐</p>''',
                        unsafe_allow_html=True)

        # Metric 3: Negative Sentiment Score
        with col3:
            st.markdown(f'''<h1 style='color:{NEGATIVE_COLOR};
                        text-align: center;'>{average_negative_score}</h1>'''
                        , unsafe_allow_html=True)
            st.markdown('''<p style='text-align: center;'>
                        Negative Sentiment Score ☹️</p>''', unsafe_allow_html=True)

        st.markdown('<hr class="horizontal-line">', unsafe_allow_html=True)

        for index, row in df.iterrows():

            with st.container():
                st.markdown(f'''<h4><span style='color:{NEWS_ARTICLE_DATE_COLOR}'>
                            {row['Date'].strftime('%B %d, %Y')} : </span><span>
                            <a href='{row['Link']}' target='_blank'
                            style='color:{NEWS_ARTICLE_COLOR}'>{row['Title']}
                            </a></span></h4>''', unsafe_allow_html=True)

                df_col1, df_col2, df_col3 = st.columns(3)
                with df_col1:
                    st.markdown(f'''<h6 style='color:{POSITIVE_COLOR}'>
                                Positive Sentiment Score: <code style='color:
                                {POSITIVE_COLOR}'>{row['Positive Sentiment Score']}
                                </code></h6>''', unsafe_allow_html=True)
                with df_col2:
                    st.markdown(f'''<h6 style='color:{NEUTRAL_COLOR}'>
                                Neutral Sentiment Score: <code style='color:
                                {NEUTRAL_COLOR}'>{row['Neutral Sentiment Score']}
                                </code></h6>''', unsafe_allow_html=True)
                with df_col3:
                    st.markdown(f'''<h6 style='color:{NEGATIVE_COLOR}'>
                                Negative Sentiment Score:<code style='color:
                                {NEGATIVE_COLOR}'>{row['Negative Sentiment Score']}
                                </code></h6>''', unsafe_allow_html=True)

                st.markdown('<hr class="horizontal-line">', unsafe_allow_html=True)

with tab4:
    selected_ticker = st.text_input('➕ Add New Ticker')
    selected_time = st.text_input('''(Optional) 🕒 Input a time period
                                  [valid formats include days ('d'), weeks ('wk'),
                                  months ('mo'), years ('y')]''')

    if st.button("🔄 Update Ticker Data"):

        selected_ticker = selected_ticker.upper()

        if len(selected_time) == 0:
            download_stock_data(selected_ticker)
        else:
            selected_time = selected_time.lower()
            if not (selected_time == 'max' or
                    selected_time[-1] in ['d','y'] or
                    selected_time[-2:] in ['wk','mo']):

                raise ValueError('''period_str formats: 'max', 'd', 'wk',
                                 'mo', 'y' (case insensitive).''')
            download_stock_data(selected_ticker, selected_time)

    if st.button("🔁 Click to Update Ticker Data to the Most Recent"):
        update_stock_data()

