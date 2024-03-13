"""
test_app.py
===========

This module contains unit tests for the UI testing of the
Streamlit Application

Classes:
    TestStreamlitApp: Test cases for the Streamlit UI.
"""

import unittest
from streamlit.testing.v1 import AppTest

class TestStreamlitApp(unittest.TestCase):
    """
    A unittest.TestCase class to test Streamlit UI
    application functionalities.

    This class contains multiple test methods to evaluate different aspects of
    the Streamlit application, such as UI elements, input validations, and data updates.

    Test Cases:
    - test_smoke_app: Test the basic functionality of the
                                Streamlit application.
    - test_number_and_titles_of_tabs: Test the titles of the tabs in the
                                Streamlit application.
    - test_stock_options: Test the stock options in the selectbox of the
                                Streamlit application.
    - test_technical_indicator_options: Test the technical indicator options in the
                                Streamlit application.
    - test_technical_indicator_length: Test the input of technical indicator length in the
                                Streamlit application.
    - test_number_of_days_input: Test the input of the number of days in the
                                Streamlit application.
    - test_percentage_change_option: Test the input of percentage change option in the
                                Streamlit application.
    - test_add_new_company_ticker_input: Test the input of a new company ticker in the
                                Streamlit application.
    - test_add_new_ticker_time_period_input: Test the input of time period for a new
                                ticker in the Streamlit application.
    - update_data_for_new_ticker: Test the update of data for a newly added
                                ticker in the Streamlit application.
    """

    def test_smoke_app(self):
        """
        Test the basic functionality of the Streamlit application.
        This test checks if the application loads without raising any exceptions.
        """
        at = AppTest.from_file("../app.py", default_timeout=10).run()
        assert not at.exception

    def test_number_and_titles_of_tabs(self):
        """
        This test verifies if the titles of the tabs match the expected labels.
        """
        at = AppTest.from_file("../app.py", default_timeout=10).run()

        expected_labels = ["📈 Stock Performance Overview",
                        "🔍 Explore Stock Technical Indicators",
                        "📰 Latest News Headlines and Articles",
                        "💡 Explore More Tickers or Update Data!"]

        for i, expected_label in enumerate(expected_labels):
            assert at.tabs[i].label == expected_label

    def test_stock_options(self):
        """
        This test verifies if there are atleast five company tickers and the
        functionality of selecting stock options.This test also verifies
        if the action on a select button successfully runs in the application.
        """
        at = AppTest.from_file("../app.py", default_timeout=10).run()
        assert len(at.tabs[0].selectbox[0].label) >= 5

        at.tabs[0].selectbox[0].select_index(0).run()
        assert not at.exception

    def test_technical_indicator_options(self):
        """
        Test the technical indicator options in the Streamlit application
        and checks the selection and value of technical indicators. This test
        also verifies if the action on a select button successfully
        runs in the application.
        """

        at = AppTest.from_file("../app.py", default_timeout=20).run()
        assert at.tabs[1].selectbox[0].label == 'Select Technical Indicator'
        assert at.tabs[1].selectbox[0].options == ["MA", "RSI", "ROC", "BBP"]

        at.tabs[1].selectbox[0].select_index(0).run()
        assert not at.exception
        assert at.tabs[1].selectbox[0].value == "MA"

        at.tabs[1].selectbox[0].select_index(1).run()
        assert not at.exception
        assert at.tabs[1].selectbox[0].value == "RSI"

    def test_technical_indicator_length(self):
        """
        Test the input of technical indicator length in the Streamlit application
        to checks the input of a numerical value for the technical
        indicator length. This test also verifies if any valid user input
        would run successfully in the application.
        """
        at = AppTest.from_file("../app.py", default_timeout=10).run()
        assert at.tabs[1].number_input[0].label == 'Input a length'
        at.tabs[1].number_input[0].set_value(5).run()
        assert not at.exception

    def test_number_of_days_input(self):
        """
        Test the input of the number of days in the Streamlit application and
        this test verifies the input of a numerical value for the number of days.
        This test also verifies if any valid user input would run s
        successfully in the application.
        """
        at = AppTest.from_file("../app.py", default_timeout=10).run()
        at.tabs[2].number_input[0].set_value(50).run()
        assert not at.exception

    def test_percentage_change_option(self):
        """
        Test the input of the percentage change in the Streamlit application
        and this test verifies the input of a numerical value for the the
        percentage change in stock price. This test also verifies if any valid
        user input would run successfully in the application.
        """
        at = AppTest.from_file("../app.py", default_timeout=10).run()
        at.tabs[2].number_input[1].set_value(-5).run()
        assert not at.exception

    def test_add_new_company_ticker_input(self):
        """
        Test the input of a new company ticker in the Streamlit application.
        This test verifies if any valid user input would run successfully in
        the application.
        """
        at = AppTest.from_file("../app.py", default_timeout=20).run()
        assert at.tabs[3].text_input[0].label == '➕ Add New Ticker'
        assert at.tabs[3].text_input[0].set_value('AMZN').run()
        assert not at.exception

    def test_add_new_ticker_time_period_input(self):
        """
        Test the input of time period for a new ticker in the Streamlit application.
        This test checks the input of a time period for a newly added ticker symbol
        and verifies if any valid user input would run successfully in the application.
        """
        at = AppTest.from_file("../app.py", default_timeout=20).run()
        at.tabs[3].text_input[1].set_value('5d').run()
        assert not at.exception

    def update_data_for_new_ticker(self):
        """
        Test the update of data for a newly added ticker in the Streamlit application.
        This test verifies the functionality of updating data for a newly added ticker.
        """
        at = AppTest.from_file("../app.py", default_timeout=20).run()
        assert at.tabs[3].button[0].label == "🔁 Click to Update Ticker Data to the Most Recent"
        at.tabs[3].button[0].click().run()
        assert not at.exception

if __name__ == '__main__':
    unittest.main()
