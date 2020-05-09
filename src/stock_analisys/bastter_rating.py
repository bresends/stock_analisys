"""
Program that  Analise the Top Rated Bastter Stocks

"""
import pandas as pd

# Defining Function to show company based on ticker


class BastterRating:

    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def company_show(self):
        """
        Pick one company and shows its information

        """

        # Open dataframe with all info
        self.df = pd.read_csv(
            'data/bastter_analysis/bastter_stocks_analised.csv')

        # Select one company from all in the DF
        self.company_info = self.df[self.df['Ticker'] == self.ticker]


stock = BastterRating('aapl')
stock.company_show()

