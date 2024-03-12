import unittest

from streamlit.testing.v1 import AppTest

class TestApp(unittest.TestCase):

    def setUp(self):
        self.at = AppTest.from_file("../app.py").run()

    def test_main_page_select_box(self):
        self.assertEqual(self.at.title[0].value, 'Cool chart!')
        select_box = self.at.tabs[0].selectbox[0]
        self.assertTrue(select_box.exists)
        select_box.select("AAPL")
        self.assertEqual(select_box.value, "AAPL")

    def test_main_page_button(self):
        button = self.at.tabs[0].button[0]
        self.assertTrue(button.exists)
        button.click()
        self.assertEqual(button.label, "Return to Initial View")

    def test_stock_performance_tab_select_box(self):
        select_box = self.at.tabs[1].selectbox[0]
        self.assertTrue(select_box.exists)

    def test_stock_performance_tab_expander(self):
        expander = self.at.tabs[1].expander[0]
        self.assertTrue(expander.exists)
        expander.click()
        self.assertTrue(expander.expanded)

    def test_news_headlines_tab_number_input(self):
        number_input = self.at.tabs[2].number_input[0]
        self.assertTrue(number_input.exists)

    def test_news_headlines_tab_button(self):
        button = self.at.tabs[2].button[0]
        self.assertTrue(button.exists)
        button.click()
        self.assertEqual(button.label, "🔄 Update Ticker Data")

    def test_explore_tickers_tab_text_input(self):
        text_input = self.at.tabs[3].text_input[0]
        self.assertTrue(text_input.exists)

    def test_explore_tickers_tab_button(self):
        button = self.at.tabs[3].button[0]
        self.assertTrue(button.exists)
        button.click()
        self.assertEqual(button.label, "🔁 Click to Update Ticker Data to the Most Recent")

if __name__ == "__main__":
    unittest.main()
