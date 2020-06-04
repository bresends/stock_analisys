import concurrent.futures
import random
import time

from bs4 import BeautifulSoup

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as time_control
from stock_analisys.packages.sql_class import MySQL


class BastterHTML:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()

    def html_open(self):
        """
        Uses Paths and HTML handling modulese to open the HTML page as a Bs4 Object
        """

        self.parsed_html = html_handling.html_file_to_bs4(
            paths.bastter_path / "full_balances_us" / f"{self.ticker}.html"
        )

    def data_extraction(self):
        self.sector = (
            self.parsed_html.find("span", class_="ativo-sector").get_text().strip()
        )
        self.industry_group = (
            self.parsed_html.find("span", class_="ativo-industry-group")
            .get_text()
            .strip()
        )
        self.industry_category = (
            self.parsed_html.find("span", class_="ativo-industry-category")
            .get_text()
            .strip()
        )
        self.exchange = (
            self.parsed_html.find("span", class_="ativo-exchange").get_text().strip()
        )

        self.description = (
            self.parsed_html.find("span", class_="ativo-description").get_text().strip()
        )
        self.origin = (
            self.parsed_html.find("span", class_="ativo-inc-country").get_text().strip()
        )

        self.market_cap = (
            self.parsed_html.find("span", class_="ativo-market-cap").get_text().strip()
        )

    def to_sql(self):
        sql_handler = MySQL()

        sql_handler.update(
            table="company_info",
            changed_column="sector",
            value=self.sector,
            where_column="ticker",
            where_equals=self.ticker,
        )

        sql_handler.update(
            table="company_info",
            changed_column="industry_group",
            value=self.industry_group,
            where_column="ticker",
            where_equals=self.ticker,
        )

        sql_handler.update(
            table="company_info",
            changed_column="industry_category",
            value=self.industry_category,
            where_column="ticker",
            where_equals=self.ticker,
        )

        sql_handler.update(
            table="company_info",
            changed_column="description",
            value=self.description,
            where_column="ticker",
            where_equals=self.ticker,
        )

        sql_handler.update(
            table="company_info",
            changed_column="market_cap",
            value=self.market_cap,
            where_column="ticker",
            where_equals=self.ticker,
        )

        sql_handler.update(
            table="company_info",
            changed_column="exchance",
            value=self.exchange,
            where_column="ticker",
            where_equals=self.ticker,
        )


def all_stocks_tickers_sql():

    """
    Grabs of tickers of companies with no Origin  
    """

    sql_handler = MySQL()

    query_response = sql_handler.stocks_db_engine.execute(
        "SELECT ticker FROM company_info"
    )
    result = tuple(x[0] for x in query_response.fetchall())

    return result


def main(ticker):

    time.sleep(random.uniform(0.1, 0.3))
    stock_obj = BastterHTML(ticker)
    print(stock_obj.ticker)
    stock_obj.html_open()
    stock_obj.data_extraction()
    stock_obj.to_sql()


if __name__ == "__main__":

    ticker_list = all_stocks_tickers_sql()

    start = time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(main, ticker_list)

    end = time.time()

    time_control.time_it_secs_conversion(start, end)
