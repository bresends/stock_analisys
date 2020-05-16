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

    # Retrieves the Table with data from the Ticker File
    def table_extract(self):
        bs4_object = html_handling.html_file_to_bs4(
            paths.fundamentei_path / "full_balances" / f"{self.ticker}.html"
        )

        # Extração da Tabela Menor
        html_balance = bs4_object.find("table", {"class": "css-xu6ppq"})

        output_rows = []

        for table_row in html_balance.findAll("tr"):
            columns = table_row.findAll("td")
            output_row = []
            for column in columns:
                output_row.append(column.get_text())
            output_rows.append(output_row)

        # Df creation from BeautifulSoup Html table
        self.company_data_df = pd.DataFrame(output_rows)

        # Empty line Removal
        self.company_data_df = self.company_data_df.drop([0], axis=0)

        # Changing Header Names
        self.company_data_df = self.company_data_df.rename(
            columns={
                0: "Year",
                1: "Equity",
                2: "Revenue",
                3: "EBITDA",
                4: "D&A",
                5: "EBIT",
                6: "Financial Results",
                7: "Taxes",
                8: "Net Income",
                9: "Net Margin",
                10: "ROE",
                11: "Cash",
                12: "Debt",
                13: "ND/EBITDA",
                14: "Operations Cash Flow",
                15: "CAPEX",
                16: "Financing Cash Flow",
                17: "Free Cash Flow",
                18: "Taxes",
                19: "Dividends",
                20: "Payout",
            }
        )

        # # Header Rename
        # df_cols = [
        #     "Year",
        #     "Equity",
        #     "Revenue",
        #     "EBITDA",
        #     "D&A",
        #     "EBIT",
        #     "Financial Result",
        #     "Taxes",
        #     "Net Income",
        #     "Net Margin",
        #     "ROE",
        #     "Cash",
        #     "Debt",
        #     "ND/EBITDA",
        #     "Cash Flow from Opeartions",
        #     "Capex",
        #     "Cash Flow from Financing",
        #     "Free Cash Flow",
        #     "Dividends",
        # ]

        # self.company_data_df.columns = df_cols


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
    evaluate_test.table_extract()


if __name__ == "__main__":
    # main_extract()
    main_evaluate()
