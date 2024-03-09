from streamlit.testing.v1 import AppTest

def test_side_bar_actions():
    at = AppTest.from_file("../app.py").run()
    assert at.sidebar.header[0].value == "Filters for Data"
    assert at.sidebar.selectbox[0].value in ['AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA']
    assert at.sidebar.selectbox[1].value in ['10%', '5%', '-5%', '-10%']

def test_tab_actions():
    at = AppTest.from_file("../app.py").run()
    at.tabs.count == 2
    at.tabs[0].button.values == 'Return to Initial View'