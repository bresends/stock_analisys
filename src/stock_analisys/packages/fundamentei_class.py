"""
Classe que lida com os objetos gerados pelo site Fundamentei
Entra autentica e salva páginas a partir de um ticker
"""

import pickle

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as prints

# =============================================================================
# Class
# =============================================================================

class Fundamentei:
    """Super Class for all related tasks for Fundamentei
    """
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url = f"https://fundamentei.com/us/{ticker}"


class FundamenteiExtract(Fundamentei):
    """
    Class related to Selenium Tasks for the Fundamentei Site
    It's a subclass of Fundamentei
    """

    def autenticate(self):
        self.driver = webdriver.Chrome(paths.bin_path / "chromedriver.exe")

        # Puxa os Cookies
        self.driver.get("https://varvy.com/pagespeed/wicked-fast.html")
        self.driver.implicitly_wait(0.2)

        for cookie in pickle.load(
            open(paths.bin_path / "cookies_fundamentei.pkl", "rb")
        ):
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)
        print("Cookies Sucessifuly Loaded")

    def html_save(self):
        """
        Saves the actual page as HTML in the Full Balances Folder
        """

        page_html = self.driver.page_source
        prints.print_line()
        print(f"HTML for {self.ticker} captured successifuly")

        with open(
            paths.data_path / "fundamentei" / "full_balances" / f"{self.ticker}.html",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(str(page_html))

    def evaluate_existence(self):
        """
        Opens a Ticker and Verify if the company existis in the Fundamentei Site
        """
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Testing URL
        try:
            print(f"Analising: {self.url}")
            page = requests.get(self.url, headers=header, timeout=5)

            # Sucessifuly Loaded
            if page.status_code == 200:
                with open(paths.fundamentei_path / "all_valid_br_stocks.txt", "a") as f:
                    f.write(f"{self.ticker} \n")
                print("Stock Appended to Valid Stocks")

            # Server Blocking Access
            elif page.status_code == 503:
                raise Exception("ServerBlock")

        except Exception as error:
            print(f"Error type [{error}] while trying to grab stock")
     
    def open_page(self):
        self.driver.get(self.url)

    def scroll_page_to_botton(self):
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")


class FundamenteiEvaluate(Fundamentei):
    """
    Class related to extrating the important data from the HTML in the list I downloaded
    It is a subclass of Fundamentei (used to treat Tickers)
    """

    def __init__(self, ticker):
        super().__init__(ticker)
        self.html_page_bs4 = html_handling.html_file_to_bs4(
            paths.fundamentei_path / "full_balances" / f"{self.ticker}.html"
        )

    # Retrieves the Table with data from the Ticker File
    def table_extract(self):

        # Full Balance Extract
        html_balance = self.html_page_bs4.find("table", {"class": "css-xu6ppq"})
        company_full_data = html_handling.table_to_pandas(html_balance)

        # Values to strings (to treat)
        company_full_data = company_full_data.applymap(str)

        # Fixing years (removing month)
        company_full_data["Year"] = company_full_data.apply(
            lambda row: row["Year"].split("/")[1], axis=1
        )

        # Treating Data (remove points and strings)
        company_full_data = company_full_data.applymap(
            lambda x: x.replace(".", "")
            .replace(",", ".")
            .replace("L", "0")
            .replace("-", "-0")
            .replace("%", "")
        )

        # Returning data to float
        company_full_data = company_full_data.applymap(float)

        # Year to int (to remove the zero in the end)
        company_full_data["Year"] = company_full_data["Year"].apply(int)

        return company_full_data

    def company_informations(self):
        pass


def main_extract():
    """
    Serves as plataform to test my script
    """

    extract_test = FundamenteiExtract("aabl")
    extract_test.autenticate()
    extract_test.open_page()
    extract_test.html_save()


def main_evaluate():
    """
    Serves as plataform to test my script
    """
    evaluate_test = FundamenteiEvaluate("mmm")
    table = evaluate_test.table_extract()
    print(table)


if __name__ == "__main__":
    # main_extract()
    main_evaluate()
