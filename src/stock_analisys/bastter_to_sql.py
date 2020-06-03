from bs4 import BeautifulSoup
import os

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths


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


if __name__ == "__main__":

    stock_obj = BastterHTML("AAPL")
    stock_obj.html_open()
    print(stock_obj.parsed_html.prettify())
