"""
Bastter Class

It extracts HTML
Sort between REITS and STOCKs
Plot Graphs

"""


# =============================================================================
# Arquivo com as funções relacionadas à classe Bastter
# =============================================================================

import pickle
import random
import time
import webbrowser

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate

import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as prints

# =============================================================================
# Class Creation
# =============================================================================


class Bastter:
    """Super Class for all related tasks for Fundamentei
    """

    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url = f"https://bastter.com/mercado/stock/{ticker}"


# =============================================================================
# Class Creation
# =============================================================================


class BastterExtract(Bastter):

    """
    Class related to Selenium Tasks for the Bastter Site
    It's a subclass of Bastter
    """

    def autenticate(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            # chrome_options=chrome_options,
            executable_path=paths.bin_path
            / "chromedriver.exe",
        )

        # Puxa os Cookies
        self.driver.get("https://varvy.com/pagespeed/wicked-fast.html")
        self.driver.implicitly_wait(0.2)

        for cookie in pickle.load(open(paths.bin_path / "cookies_bastter.pkl", "rb")):
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)
        print("Cookies Sucessifuly Loaded")

    def consolidated_data_click(self):

        """
        Clicks to the consolidated button (testing if it exists)
        """

        consolidated_button = self.driver.find_element_by_xpath(
            '//*[@id="quadro-completo-menu"]'
        )

        # Se está carregado, passa pra frente, senão para.
        if consolidated_button.is_displayed():

            self.driver.find_element_by_xpath('//*[@id="quadro-completo-menu"]').click()

        else:

            print("Button not found in page")

    def html_save(self):
        """
        Saves the actual page as HTML in the Full Balances Folder
        """

        page_html = self.driver.page_source
        prints.print_line()
        print(f"HTML for {self.ticker} captured successifuly")

        with open(
            paths.data_path / "bastter" / "full_balances_us" / f"{self.ticker}.html",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(str(page_html))

    def open_page(self):
        self.driver.get(self.url)

    def scroll_page_to_botton(self):
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")

    def evaluate_existence(self):

        """
        Opens a Ticker and Verify if the company existis in the Fundamentei Site
        """

        page_html = self.driver.page_source

        bs4 = BeautifulSoup(page_html, "lxml")

        stock_not_found = bs4.find(text="Stock not found.")

        if not stock_not_found:
            with open(paths.bastter_path / "all_valid_us_stocks.txt", "a") as f:
                f.write(f"{self.ticker} \n")
            print(f"Stock {self.ticker} Found")

        self.driver.quit()


# =============================================================================
# HTML Extract
# =============================================================================


class BastterEvaluate(Bastter):

    """
    Class related to extrating the important data from the HTML in the list I downloaded
    It is a subclass of Fundamentei (used to treat Tickers)
    """

    def __init__(self, ticker):
        super().__init__(ticker)
        self.html_page_bs4 = html_handling.html_file_to_bs4(
            paths.bastter_path / "full_balances_us" / f"{self.ticker}.html"
        )

    def tables_extract(self):

        """
        Retrieves the Table with data from the Ticker File
        """

        # Removing percentual values
        for span_tag in self.html_page_bs4.findAll("span", {"class": "varperc"}):
            span_tag.replace_with("")

        # Filtering Tables
        all_tables = self.html_page_bs4.find_all(
            "table",
            {"class": "evanual quadro table table-striped table-hover marcadagua"},
        )

        dre = html_handling.table_to_pandas(all_tables[1])
        cf = html_handling.table_to_pandas(all_tables[2])
        mult = html_handling.table_to_pandas(all_tables[3])

        def treat_tables(table):

            # Values to strings (to treat)
            table = table.applymap(str)

            # Treating Data (remove points and strings)
            table = table.applymap(
                lambda x: x.replace(".", "")
                .replace(",", ".")
                .replace("L", "0")
                .replace("-", "-0")
                .replace("%", "")
                .replace("20 TTM", "2020")
            )

            table = table.transpose()
            table = table.reset_index()
            table = table.drop(1, axis=0)
            table = table.reset_index(drop=True)

            # Fixing Header
            new_header = table.iloc[0]  # grab the first row for the header
            table = table[1:]  # take the data less the header row
            table.columns = new_header  # set the header row as the df header
            table.columns.values[0] = "Year"

            # Returning data to float
            table = table.applymap(float)

            # Year to int (to remove the zero in the end)
            table["Year"] = table["Year"].apply(int)

            table.sort_values(by=["Year"], inplace=True, ascending=True)
            table = table.reset_index(drop=True)

            return table

        # Adding Important values to DRIE
        dre = treat_tables(dre)
        dre = percentual_variance(dataframe=dre, field="Net Income")

        cash_flow = treat_tables(cf)
        multiples = treat_tables(mult)

        return (dre, cash_flow, multiples)


# =============================================================================
# Useful Functions
# =============================================================================


def percentual_variance(dataframe, field):

    """Grabs dataframe and evaluates a percentual change in values in any seires

    Returns:
        dataframe -- the same dataframe with a new column with the percentual changes of the selected field
    """

    lists = []

    # Grabs the first Net income in the original table
    last_year_value = dataframe.loc[0, field]

    for current_year_value in dataframe[field]:

        # Divide o valor do ano pelo valor do ano anterior
        percentual_change = int(
            (current_year_value - last_year_value) / (abs(last_year_value + 1)) * 100
        )

        # Adiciona na lista
        lists.append(percentual_change)

        # Faz com que o valor do ano anterior pego o do ano analisado
        last_year_value = current_year_value + 0.01

    dataframe[f"%-{field}"] = lists

    return dataframe


def main_extract(ticker):
    """
    Makes requests and pulls the data from the site
    """
    extract_test = BastterExtract(ticker)
    extract_test.autenticate()
    extract_test.open_page()
    extract_test.consolidated_data_click()
    extract_test.html_save()


def main_evaluate(ticker):
    """
    Show the Dataframes from the Downloaded HTML Bastter Files
    """

    evaluate_test = BastterEvaluate(ticker)
    tables = evaluate_test.tables_extract()

    display(tables[0])
    display(tables[1])
    display(tables[2])


if __name__ == "__main__":
    # main_extract("mmm")
    main_evaluate("mmm")
