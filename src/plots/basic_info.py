"""
Plot generating Module

"""
import matplotlib.pyplot as plt
import pandas as pd

import stock_analisys.packages.sql_class as sql_class


class Plots:
    def __init__(self, ticker):
        # Ticker
        self.ticker = ticker.lower()

        # SQL Connectors
        self.__stocks_general_info = sql_class.MySQL("stocks_general_info").engine
        self.__bastter_conn = sql_class.MySQL("bastter").engine
        self.__fundamentei_conn = sql_class.MySQL("fundamentei").engine
        self.__morning_star_con = sql_class.MySQL("morning_star").engine

        # Tables
        self.__bastter_full_balance = pd.read_sql_table(
            f"{self.ticker}_full_balance", self.__bastter_conn
        )

    def pull_basic_info(self):
        """
        Grabs the Company Info from MySQL 
        """

        query = f""" \
        SELECT * \
        FROM company_info \
        WHERE ticker = '{self.ticker.upper()}' \
        """
        self.company_info = pd.read_sql_query(query, self.__stocks_general_info)

    def show_info(self):
        """
        Plots Income, EBit and Ebitda for Bastter
        """

        self.pull_basic_info()

        return self.company_info


def main(ticker):
    stock = Plots(ticker)
    info = stock.show_info()

    display(info.iloc[:, [1, 2, 3, 5, 6, 8, 9, 10]])
    print("")

    try:
        mk_cap = float(info.iloc[0, 4])
        display("${:,.2f}".format(mk_cap))
    except ValueError:
        display(info.iloc[0, 4])

    print("")

    display(info.iloc[0, 12])


if __name__ == "__main__":
    main("aapl")
