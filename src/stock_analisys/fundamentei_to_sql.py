"""
Scrapes the HTML and put information inside DB
"""

import re
import time

from bs4 import BeautifulSoup

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths
from stock_analisys.packages.sql_connection import sql_engine


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
        self.fundation_year = int(
            self.parsed_html.find_all("div", class_="css-1bcdh3w")[0]
            .get_text()
            .split()[0]
        )
        self.ipo_year = int(
            self.parsed_html.find_all("div", class_="css-1bcdh3w")[1]
            .get_text()
            .split()[0]
        )

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


if __name__ == "__main__":

    files = html_handling.list_files(paths.fundamentei_path / "full_balances_us")
    tickers = list(map(lambda x: x.split(".")[0], files))

    for item in tickers:
        print(item)

        try:
            stock = FundamenteiToSql(item)
            stock.html_open()
            stock.info_extract()
            stock.to_sql()
            print("Stock Succesifuly Stored")
            print(stock)

        except Exception as erro:
            print("Error. Trowing Stock to not retrivable MySQL database")
            print(type(erro))
            print(erro.args)
            print(erro)
            cursor = sql_engine.connect()

            query = f"""\
            INSERT INTO not_retrivable(\
                ticker,\
                company_name\
                )\
            VALUES(\
                '{stock.ticker}',\
                '{stock.company_name}'\
                );"""

            cursor.execute(query)
