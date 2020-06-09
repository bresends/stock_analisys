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
        self.full_balance = pd.read_sql_table(
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
        self.company_info_full_balance = pd.read_sql_query(
            query, self.__stocks_general_info
        )

    def bastter_var_var_eps(self):
        """
        Plots Income, EBit and Ebitda for Bastter
        """

        self.pull_basic_info()

        # Setting Fig
        fig = plt.figure()
        fig.set_size_inches(10, 6)

        fig.suptitle(
            f"{self.ticker.upper()} - {self.company_info_full_balance['company_name'][0]}",
            fontsize=14,
            fontweight="bold",
        )

        plot = fig.add_subplot(111)

        # ==========================================================
        # Income & EBIT plot
        # ==========================================================
        var_pos = self.full_balance[self.full_balance["var_eps"] >= 0]
        var_neg = self.full_balance[self.full_balance["var_eps"] <= 1]

        plot.bar(
            var_pos["yr"], var_pos["var_eps"], color="skyblue", label="(-) EPS % ",
        )

        plot.bar(
            var_neg["yr"], var_neg["var_eps"], color="red", label="(+) EPS % ",
        )

        # Zero mark
        plot.axhline(y=0, color="red", linestyle="--", marker=".", markersize=10)
        plot.axhline(y=10, color="indigo", linestyle="--", marker=".", markersize=10)

        plot.set_title(
            "EPS % - Bastter", fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel("EPS %  ", color="black")
        plot.grid()
        plot.legend()

        plt.show()

        plt.show()


def main(ticker):
    stock = Plots(ticker)
    stock.bastter_var_var_eps()


if __name__ == "__main__":
    main("aapl")
