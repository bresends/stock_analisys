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


class FundamenteiToSql:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()

    def html_open(self):
        """
        Uses Paths and HTML handling modulese to open the HTML page as a Bs4 Object
        """
        self.parsed_html = html_handling.html_file_to_bs4(
            paths.fundamentei_path
            / "full_balances_us"
            / f"{self.ticker.strip().upper()}.html"
        )

    def info_extract(self):
        """
        Takes the HTML BS4 object and grabs the important data 
        """
        self.company_name = self.parsed_html.h1.get_text().replace("'", "")

        self.ipo_year = int(
            self.parsed_html.find_all("div", class_="css-1bcdh3w")[0]
            .get_text()
            .split()[0]
        )

        self.fundation_year = int(self.ipo_year - 5)

        # CIK number retrieval
        _page_links = self.parsed_html.find_all("a", class_="css-e08q0q")

        for item in _page_links:
            if "sec" in item["href"]:  # In all links search for the SEC word
                self.cik = re.findall("\d+", item["href"])[0]

        # IR url retrieval
        self.ir_url = self.parsed_html.find_all("a", class_="css-e08q0q")[1]["href"]

    def to_sql(self):
        """
        Saves Extracted data to MySQL 
        """
        cursor = sql_engine.connect()

        query = f"""\
        INSERT INTO company_info(\
            ticker,\
            company_name,\
            ipo_year, \
            fundation_year,\
            cik_number,\
            ri_site\
            )\
        VALUES(\
            '{self.ticker}',\
            '{self.company_name}',\
            '{self.ipo_year}',\
            '{self.fundation_year}',\
            '{self.cik}',\
            '{self.ir_url}'\
            );"""

        cursor.execute(query)

    def __str__(self):
        return f"{self.ticker} - {self.company_name} - IPO: {self.ipo_year} - Fundation {self.fundation_year} - CIK {self.cik}"


def dump_to_sql(ticker):
    """
    Receives Ticker
    Grabs HTML file
    """

    stock = FundamenteiToSql(ticker)
    stock.html_open()
    stock.info_extract()
    stock.to_sql()
    print("Stock Succesifuly Stored")
    print(stock)


def problem_fundamentei(position):

    try:
        df = pd.read_sql("SELECT * FROM trash_stocks", con=sql_engine)

        ticker = df["ticker"].iloc[position]

        print(ticker)

        dump_to_sql(ticker)

        cursor = sql_engine.connect()

        query = f"""DELETE FROM trash_stocks WHERE ticker = '{ticker}';"""

        cursor.execute(query)

    except IndexError:

        # webbrowser.open_new_tab(f"https://fundamentei.com/us/{ticker}")
        pass


if __name__ == "__main__":

    dump_to_sql("appl")
