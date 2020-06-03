"""
Scrapes the HTML and put information inside DB
"""

import re
import time
import webbrowser

import pandas as pd
from bs4 import BeautifulSoup

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths
from stock_analisys.packages.sql_class import MySQL


class FundamenteiToSql:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()

    def html_open(self):
        """
        Uses Paths and HTML handling modulese to open the HTML page as a Bs4 Object
        """
        self.parsed_html = html_handling.html_file_to_bs4(
            paths.fundamentei_path / "full_balances_us" / f"{self.ticker}.html"
        )

    def info_extract(self):
        """
        Takes the HTML BS4 object and grabs the important data 
        """
        self.company_name = self.parsed_html.h1.get_text().replace("'", "")

        # Extracting Orign 
        self.origin = self.parsed_html.find('img', class_='css-1phd9a0')['alt']


    def to_sql(self):
        sql_handler = MySQL()

        sql_handler.update(
            table="company_info",
            changed_column="origin",
            value=self.origin,
            where_column="ticker",
            where_equals=self.ticker,
        )

    def __str__(self):
        return f"{self.ticker} - Origin : {self.origin}"


def dump_to_sql(ticker):
    """
    Receives Ticker
    Grabs HTML file
    """

    stock = FundamenteiToSql(ticker)
    stock.html_open()
    stock.info_extract()
    stock.to_sql()
    print("Stock Succesifuly Updated")
    print(stock)


if __name__ == "__main__":

    """
    Grabs of tickers of companies with no Origin  
    """

    sql_handler = MySQL()

    result = sql_handler.select_unique_column(
        table="company_info",
        desired_column="ticker",
        where_column="origin",
        where_equals="{{inc-country}}",
    )

    # Uses this to extract Origins 

    for i in range(100):
        dump_to_sql(result[i])
