import concurrent.futures
import time
import random

from bs4 import BeautifulSoup
from selenium import webdriver

import stock_analisys.packages.paths as paths
from stock_analisys.packages.sql_class import MySQL
import stock_analisys.packages.prints as time_control


class Yahoo:
    def __init__(self, ticker):
        self.ticker = ticker.strip().upper()
        self.base_url = f"https://finance.yahoo.com/quote/{self.ticker}"
        self.profile_url = (
            f"https://finance.yahoo.com/quote/{self.ticker}/profile?p={self.ticker}"
        )

    def __str__(self):
        return f"Yahoo({self.ticker})"

    def get_html(self, url):

        self.driver = webdriver.Chrome(
            # chrome_options=chrome_options,
            executable_path=str(paths.bin_path / "chromedriver.exe"),
        )

        self.driver.get(url)

        page_html = self.driver.page_source

        time.sleep(1)

        self.soup = BeautifulSoup(page_html, "lxml")

        self.driver.quit()

    def sector_extract(self):
        try:
            self.sector = (
                self.soup.find_all("span", class_="Fw(600)")[0].get_text().strip()
            )
            self.industry_category = (
                self.soup.find_all("span", class_="Fw(600)")[1].get_text().strip()
            )
            self.description = self.soup.find("p", class_="Mt(15px) Lh(1.6)").get_text()

        except IndexError as err:

            print(f"Error {err} - Setting All to Null")
            self.sector = "{{sector}}"
            self.industry_category = "{{industry_category}}"
            self.sector = "{{description}}"

    def to_sql(self):

        sql_handler = MySQL()

        sql_handler.update(
            table="company_info",
            changed_column="description",
            value=self.description,
            where_column="ticker",
            where_equals=self.ticker,
        )


"""
Misc Functions 
"""


def custom_ticker_search():

    querry = MySQL()
    query_response = querry.stocks_db_engine.execute(
        "SELECT ticker FROM company_info WHERE `description` IS NULL or `description` = 'N/A' or `description` = '{{description}}';"
    )
    result = tuple(x[0] for x in query_response.fetchall())
    return result


def main(ticker):

    time.sleep(random.uniform(0.1, 0.2))
    stock = Yahoo(ticker)
    print(stock)
    stock.get_html(stock.profile_url)
    stock.sector_extract()
    stock.to_sql()
    print("Stock Succesifuly Updated")


if __name__ == "__main__":

    mk = custom_ticker_search()

    start = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        results = executor.map(main, mk)

    end = time.time()

    time_control.time_it_secs_conversion(start, end)
