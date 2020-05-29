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
    """
    Super Class for all related tasks for Fundamentei
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
            paths.data_path
            / "fundamentei"
            / "full_balances_us"
            / f"{self.ticker}.html",
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
            paths.fundamentei_path / "full_balances_us" / f"{self.ticker}.html"
        )

    def table_extract(self):

        """
        Retrieves the Table with data from the Ticker File
        """
        # Full Balance Extract
        html_balance = self.html_page_bs4.find("table", {"class": "css-xu6ppq"})
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
            .replace("20 TTM", "2020")
        )

        # Returning data to float
        self.company_full_data = self.company_full_data.applymap(float)

        # Year to int (to remove the zero in the end)
        self.company_full_data["Year"] = self.company_full_data["Year"].apply(int)

    def income_percentual(self):

        """
        Evaluates drops in revenue year from year
        """

        income_list = []

        # Grabs the first Net income in the original table
        income_last_year = self.company_full_data.loc[0, "Net Inc."]

        for income_current_year in self.company_full_data["Net Inc."]:

            # Divide o lucro do ano pelo lucro do ano anterior
            percentual_change = int(
                (income_current_year - income_last_year)
                / (abs(income_last_year + 1))
                * 100
            )

            # Adiciona na lista
            income_list.append(percentual_change)

            # Faz com que o valor do ano anterior pego o do ano analisado
            income_last_year = income_current_year + 0.01

        self.company_full_data["%"] = income_list
        
    def company_informations(self):
        """
        Grabs the Company basic info
        """
        self.name = self.html_page_bs4.h1.get_text()
        self.fundation = self.html_page_bs4.find_all("div", "css-1bcdh3w")[0].get_text()
        self.ipo = self.html_page_bs4.find_all("div", "css-1bcdh3w")[1].get_text()
        self.market_cap = self.html_page_bs4.find("div", "css-1izgaab").get_text()
        self.industry = self.html_page_bs4.find("a", class_="css-e08q0q").get_text()
        self.description = self.html_page_bs4.find("div", "css-amw407").get_text()


def main_extract():
    """
    Serves as plataform to test my script
    """

    extract_test = FundamenteiExtract("DISCA")
    extract_test.autenticate()
    extract_test.open_page()
    extract_test.html_save()


def main_evaluate():
    """
    Serves as plataform to test my script
    """

    evaluate_test = FundamenteiEvaluate("aapl")
    evaluate_test.table_extract()
    evaluate_test.income_percentual()
    evaluate_test.company_informations()


if __name__ == "__main__":
    # main_extract()
    main_evaluate()
