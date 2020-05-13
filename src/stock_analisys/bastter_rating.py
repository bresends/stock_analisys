"""
Program that  Analise the Top Rated Bastter Stocks

"""

import webbrowser
from pathlib import Path

import pandas as pd

import stock_analisys.packages.bastter_class as bastter_class
import stock_analisys.packages.plots as plots

# =============================================================================
# Directories Setup
# =============================================================================

cwd_path = Path.cwd()
data_path = cwd_path / "data"
bin_path = cwd_path / "bin"


def ticker_selection():
    selected = input("Pick the analised company: ")
    return selected


def setor_extract(ticker):
    """
    Pulls the company Sector if it was not found in stocks_analised
    """

    company_object = bastter_class.BastterStocks(ticker)
    company_object.autenticate()
    company_object.company_data_extract()

    sector = company_object.sector
    company_country = company_object.company_country
    industry_group = company_object.industry_group
    industry_category = company_object.industry_category
    company_name_html = company_object.company_name

    company_object.quit_driver()

    return (
        company_country,
        sector,
        industry_group,
        industry_category,
        company_name_html,
    )


class Company:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()

    def __repr__(self):

        return f"Company Instaciated: {self.ticker}"

    def data_retrieve(self):

        """
        Function from the object that finds the file with the company data
        It open the folder and try to find the file
        If not found it grabs the data from Bastter
        """

        simplified_balances_path = data_path / "simplified_balances"

        # Read all the files in the Simplified Balances folder
        files = [item for item in simplified_balances_path.iterdir() if item.is_file()]

        for item in files:

            item = str(item)
            full_name = item.split("\\")[-1]
            ticker_control = full_name.split("-")[0].strip()

            if self.ticker == ticker_control:

                self.simple_balance = pd.read_csv(
                    data_path / "simplified_balances" / full_name
                )

                # Extracts the name of the company
                self.company_name = item.split("-")[1]
                print(f"Found: {self.company_name}")
                break
        else:
            print("Simple balance file not found - Stock not downloaded yet")
            self.simple_balance = pd.DataFrame()

    def data_info_to_clipboard(self):

        """
        Funtion that finds the Company data for a given Ticker
        It picks the retrieved data from stocks_analised and gives back to the user
        """

        bastter_stocks_analised = pd.read_csv(
            data_path / "bastter_analysis" / "bastter_stocks_analised.csv"
        )

        data_info = bastter_stocks_analised[
            bastter_stocks_analised["Ticker"] == self.ticker
        ]

        # If the dataframe is not empty
        if not data_info.empty:
            print("############# Info in clipboard #############")
            data_info.to_clipboard(excel=True, index=False, header=False)

        else:
            
            print(" ----- Grabing Data ------ ")

            # Uses function to grab the data
            company_info = setor_extract(self.ticker)

            """ Try the grab data from the simple balance
                If the file does not exist, it set the loss and flags
            """
            try:
                motive = ""

                # Contagem dos anos de prejuízo
                loss = [item for item in self.simple_balance["Net Income"] if item <= 0]
                drop = [item for item in self.simple_balance["%"] if item < 0]

                "Flags Foreign Companies"
                if company_info[0] != "USA":
                    flag = "foreign company"

                "Flags Companies with a drop in last year Profits"
                if (
                    self.simple_balance["Net Income"].iloc[-1]
                    < self.simple_balance["Net Income"].iloc[-2]
                ):
                    flag = "last year drop"
                    motive = "Lucros Inconsistentes"
                else:
                    flag = ""

                "Flags Companies with High Debt"
                for item in self.simple_balance["ND/EBITDA"]:
                    if item > 3:
                        flag = "high debt"
                        motive = "Dívida"

                "Flags Companies with Losses"
                for item in self.simple_balance["Net Income"]:
                    if item < 0:
                        flag = "loss"

            except KeyError as erro:

                print(
                    f" {erro} - The simple balance for this stock was not downloaded - Only picking Company Info "
                )

                drop = ""
                loss = ""
                flag = ""
                self.company_name = company_info[4]
                webbrowser.open(f"https://bastter.com/mercado/stock/{self.ticker}")

            stock_info_dict = {
                "Ticker": self.ticker,
                "Origin": company_info[0],
                "Company": self.company_name,
                "Sector": company_info[1],
                "Group": company_info[2],
                "Category": company_info[3],
                "Loss": len(loss),
                "Income Drop": len(drop),
                "Flag": flag,
                "Motive": motive,
            }

            df_individual_stock = pd.DataFrame.from_dict(
                stock_info_dict, orient="index"
            )
            df_individual_stock = df_individual_stock.transpose()

            print("############# Info in clipboard #############")
            df_individual_stock.to_clipboard(excel=True, index=False, header=False)

            "Apends to the Bastter_stocks_Analised"
            df_individual_stock = df_individual_stock.drop(columns=['Motive'], axis=1)
            
            df_individual_stock.to_csv(
                data_path / "bastter_analysis" / "bastter_stocks_analised.csv",
                index=False,
                header=False,
                mode="a",
            )

    def plot_income(self):

        if not self.simple_balance.empty:

            plots.data_graph(self.simple_balance, self.ticker, self.company_name)


if __name__ == "__main__":

    # Instaciate objetct
    stock_picked = ticker_selection()
    stock_object = Company(stock_picked)

    # Methods
    stock_object.data_retrieve()
    stock_object.data_info_to_clipboard()
    stock_object.plot_income()
