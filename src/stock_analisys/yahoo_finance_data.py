import time

from bs4 import BeautifulSoup
from selenium import webdriver

import stock_analisys.packages.paths as paths
from stock_analisys.packages.sql_class import MySQL


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

    def mkt_cap_extract(self):

        data_table = self.soup.find("table", class_="W(100%) M(0) Bdcl(c)")

        # Verify if data_table has anything. If not mkt Cap = 0
        if data_table:
            mkt_cap_raw = data_table.find("span", class_="Trsdu(0.3s)").get_text()

            # Treat mkt_cap
            if "M" in mkt_cap_raw:
                mkt_cap_raw = mkt_cap_raw.replace("M", "")
                self.mkt_cap = int(float(mkt_cap_raw.split()[0]) * 1000000)

            elif "B" in mkt_cap_raw:
                mkt_cap_raw = mkt_cap_raw.replace("B", "")
                self.mkt_cap = int(float(mkt_cap_raw.split()[0]) * 1000000000)

            elif "0" in mkt_cap_raw:
                self.mkt_cap = 0

        else:
            self.mkt_cap = 0
    
    def sector_extract(self):
        pass 

    def to_sql(self):

        sql_handler = MySQL()

        sql_handler.update(
            table="company_info",
            changed_column="sector",
            value=self.mkt_cap,
            where_column="ticker",
            where_equals=self.ticker,
        )


"""
Misc Functions 
"""

def custom_ticker_search():
    
    querry = MySQL()
    query_response = querry.stocks_db_engine.execute("SELECT ticker FROM company_info WHERE sector IS NULL or sector = '{{setor}}' or sector = 'N/D' or sector = '-';")
    result = tuple(x[0] for x in query_response.fetchall())
    return result


def main(ticker):

    stock = Yahoo(ticker)
    print(stock)
    stock.get_html(stock.profile_url)
    stock.sector_extract()
    stock.to_sql()
    stock.driver.quit()
    print("Stock Succesifuly Updated")


if __name__ == "__main__":

    mk = custom_ticker_search()
    
    for i in mk:
        main(i)
