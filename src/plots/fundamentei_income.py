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
            f"{self.ticker}_full_balance", self.__fundamentei_conn
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
        self.company_info___bastter_full_balance = pd.read_sql_query(
            query, self.__stocks_general_info
        )

    def fundamentei_income(self):
        """
        Plots Income, EBit and Ebitda for Bastter
        """

        self.pull_basic_info()

        # Setting Fig
        fig = plt.figure()
        fig.set_size_inches(10, 6)

        fig.suptitle(
            f"{self.ticker.upper()} - {self.company_info___bastter_full_balance['company_name'][0]}",
            fontsize=14,
            fontweight="bold",
        )

        plot = fig.add_subplot(111)

        # ==========================================================
        # Income & EBIT plot
        # ==========================================================
        plot.bar(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["ebitda"],
            color="orange",
            alpha=0.9,
            label="EBITDA",
        )

        plot.bar(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["ebit"],
            color="gold",
            alpha=1,
            label="EBIT",
        )

        plot.plot(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["net_income"],
            color="forestgreen",
            linestyle="-",
            marker=".",
            markersize=8,
        )

        # Zero mark
        plot.axhline(y=0, color="red", linestyle="--", marker=".", markersize=10)

        # Fill Between Profit
        plot.fill_between(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["net_income"],
            where=(self.__bastter_full_balance["net_income"] > 0),
            color="g",
            alpha=1,
            interpolate=True,
            label="Profit",
        )

        # Fill Between Loss
        plot.fill_between(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["net_income"],
            where=(self.__bastter_full_balance["net_income"] < 0),
            color="r",
            alpha=0.95,
            interpolate=True,
            label="Loss",
        )

        plot.set_title(
            "[Net Income] - Fundamentei", fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel("Net Income (mil)", color="black")
        plot.grid()
        plot.legend()
        plt.show()


def main(ticker):
    stock = Plots(ticker)
    stock.fundamentei_income()


if __name__ == "__main__":
    main("aapl")
