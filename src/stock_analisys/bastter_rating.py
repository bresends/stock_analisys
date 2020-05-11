"""
Program that  Analise the Top Rated Bastter Stocks

"""

from pathlib import Path

import pandas as pd

import stock_analisys.packages.plots as plots

# =============================================================================
# Directories Setup
# =============================================================================

cwd_path = Path.cwd()
data_path = cwd_path / 'data'
bin_path = cwd_path / 'bin'


def ticker_selection():
    selected = input('Pick the analised company: ')
    return selected


class Company:

    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def __repr__(self):

        return f'Company Instaciated: {self.ticker}'

    def data_retrieve(self):
        """
        Function from the object that finds the file with the company data
        It open the folder and try to find the file
        If not found it grabs the data from Bastter
        """

        simplified_balances_path = data_path / 'simplified_balances'

        # Read all the files in the Simplified Balances folder
        files = [item for item in simplified_balances_path.iterdir()
                 if item.is_file()]

        for item in files:
            item = str(item)
            item = item.split('\\')[-1]

            if self.ticker in item:

                self.simple_balance = pd.read_csv(
                    data_path / 'simplified_balances' / item)

                # Extracts the name of the company
                self.company_name = item.split('-')[1]
                print(self.company_name)
                break
        else:
            print('Stock not downloaded yet')
            self.simple_balance = pd.DataFrame()

    def plot_income(self):

        if not self.simple_balance.empty:

            plots.data_graph(
                self.simple_balance,
                self.ticker,
                self.company_name)
        else:
            print('Not possible to print. File with the data does not exist')


if __name__ == '__main__':
    stock_picked = ticker_selection()
    stock_object = Company(stock_picked)
    stock_object.data_retrieve()
    stock_object.plot_income()
