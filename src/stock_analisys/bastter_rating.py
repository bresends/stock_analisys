"""
Program that helps in the Bastter Stock Rating Analysis

"""
import pandas as pd
from tabulate import tabulate
import sys

print(sys.path)

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
            'data/avaliações_bastter/bastter_stocks_analised.csv')

        # Select one company from all in the DF
        self.company_info = self.df[self.df['Ticker'] == self.ticker]

        # Print selected company info
        print(tabulate(self.company_info.head(), headers='keys', tablefmt='psql'))


stock = BastterRating('aapl')
stock.company_show()
