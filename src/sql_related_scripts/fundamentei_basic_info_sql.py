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
        # self.company_name = self.parsed_html.h1.get_text().replace("'", "")

        # # Extracting Orign
        # self.origin = self.parsed_html.find("img", class_="css-1phd9a0")["alt"]

        # Extract Market Cap
        mkt_cap_raw = self.parsed_html.find("div", class_="css-1izgaab").get_text()

        if "Mi" or "mi" in mkt_cap_raw:
            self.mkt_cap = int(mkt_cap_raw.split()[0]) * 1000000

        elif "Bi" or "bi" in mkt_cap_raw:
            self.mkt_cap = int(mkt_cap_raw.split()[0]) * 1000000000

        elif "Tri" or "tri" in mkt_cap_raw:
            self.mkt_cap = int(mkt_cap_raw.split()[0]) * 1000000000000

    def to_sql(self):
        sql_handler = MySQL()

        sql_handler.update(
            table="company_info",
            changed_column="market_cap",
            value=self.mkt_cap,
            where_column="ticker",
            where_equals=self.ticker,
        )

    def __str__(self):
        return f"{self.ticker}"


def dump_to_sql(ticker):
    """
    Receives Ticker
    Grabs HTML file
    """

    try:
        stock = FundamenteiToSql(ticker)
        print(stock)
        stock.html_open()
        stock.info_extract()
        stock.to_sql()
        print("Stock Succesifuly Updated")
    except :
        pass
    


def market_cap_no_info_list():

    """
    Grabs of tickers of companies with no Market Cap
    """

    sql_handler = MySQL()

    result = sql_handler.select_unique_column(
        table="company_info",
        desired_column="ticker",
        where_column="market_cap",
        where_equals="{{market-cap}}",
    )

    return result


if __name__ == "__main__":

    mk = market_cap_no_info_list()
    
    for item in mk:
        dump_to_sql(item)
