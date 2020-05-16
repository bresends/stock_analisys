"""
Classe que lida com os objetos gerados pelo site Fundamentei
Entra autentica e salva páginas a partir de um ticker
"""

import pickle

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths

# =============================================================================
# Class
# =============================================================================


class FundamenteiExtract:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url = f"https://fundamentei.com/us/{ticker}"

    def open_page(self):
        self.driver.get(self.url)

    def autenticate(self):

        self.driver = webdriver.Chrome(paths.bin_path / "chromedriver.exe")

        # Puxa os Cookies
        self.driver.get("https://varvy.com/pagespeed/wicked-fast.html")
        self.driver.implicitly_wait(0.5)

        for cookie in pickle.load(
            open(paths.bin_path / "cookies_fundamentei.pkl", "rb")
        ):
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)
        print("Cookies Sucessifuly Loaded")

    def html_save(self):
        page_html = self.driver.page_source
        print("Captured")

        with open(
            paths.data_path / "fundamentei" / "full_balances" / f"{self.ticker}.html",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(str(page_html))


class FundamenteiEvaluate(FundamenteiExtract):
    """
    Class related to extrating the important data from the HTML in the list I downloaded
    """

    # Retrieves the Table with data from the Ticker File
    def table_extract(self):

        bs4_object = html_handling.html_file_to_bs4(
            paths.fundamentei_path / "full_balances" / f"{self.ticker}.html"
        )

        # Full Balance Extract
        html_balance = bs4_object.find("table", {"class": "css-xu6ppq"})
        self.company_full_data = html_handling.table_to_pandas(html_balance)

        # Values to strings (to treat)
        self.company_full_data = self.company_full_data.applymap(str)

        # Fixing years (removing month)
        self.company_full_data["Year"] = self.company_full_data.apply(
            lambda row: row["Year"].split("/")[1], axis=1
        )

        # Treating Data (remove points and strings)
        self.company_full_data = self.company_full_data.applymap(
            lambda x: x.replace(".", "")
            .replace(",", ".")
            .replace("L", "0")
            .replace("-", "-0")
            .replace("%", "")
        )

        # Returning data to float
        self.company_full_data = self.company_full_data.applymap(float)

        # Year to int (to remove the zero in the end)
        self.company_full_data["Year"] = self.company_full_data["Year"].apply(int)
    
    def plots(self):
        


def main_extract():
    """
    Serves as plataform to test my script
    """

    extract_test = FundamenteiExtract("amzn")
    extract_test.autenticate()
    extract_test.open_page()
    extract_test.html_save()


def main_evaluate():
    """
    Serves as plataform to test my script
    """
    evaluate_test = FundamenteiEvaluate("amzn")
    table = evaluate_test.table_extract()


if __name__ == "__main__":
    # main_extract()
    main_evaluate()
