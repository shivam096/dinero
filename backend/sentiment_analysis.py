import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer



titles = [
    "Dow Jones Futures: Fed Meeting On Deck; AI Stock Supermicro Surges 10% On Earnings Beat.",
    "Tech earnings, JOLTS data: What to Watch.",
    "Stocks Pick Up Afternoon Steam To End At Day's Highs; Dow And S&P Close At New Records",
    "Microsoft names 'Call of Duty' executive Johanna Faries as Blizzard's president.",
    'These Stocks Are Moving the Most Today: SoFi, iRobot, Tesla, Archer Daniels, McGrath RentCorp, ZoomInfo, and More',
    'Cathie Wood Likes UiPath, IBD Stock Of The Day, As AI Play. But Some Analysts See Microsoft Risk.',
    'Forget The Magnificent Seven. Focus On These Fab Five.',
    'Magnificent Seven Stocks To Buy And Watch: Nvidia, Tesla Rally'
]



def get_sentiment_value(title_list: list) -> dict:
    senti_dict = {}
    analyzer = SentimentIntensityAnalyzer()
    for sentence in titles:
        vs = analyzer.polarity_scores(sentence)
        senti_dict[sentence] = vs
    
    return senti_dict


print(get_sentiment_value(title_list=titles))