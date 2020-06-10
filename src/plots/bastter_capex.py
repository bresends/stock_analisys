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
        self.company_info___bastter_full_balance = pd.read_sql_query(
            query, self.__stocks_general_info
        )

    def bastter_income(self):
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

        plot.plot(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["capex_fco"],
            color="goldenrod",
            linestyle="-",
            marker=".",
            markersize=8,
        )

        # Zero mark
        plot.axhline(y=30, color="red", linestyle="--", marker=".", markersize=10)
        plot.axhline(y=70, color="red", linestyle="--", marker=".", markersize=10)
        plot.axhline(y=100, color="red", linestyle="--", marker=".", markersize=10)
        plot.axhline(y=130, color="red", linestyle="--", marker=".", markersize=10)

        # Fill Between Profit
        plot.fill_between(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["capex_fco"],
            where=(self.__bastter_full_balance["capex_fco"] > 0),
            color="gold",
            alpha=1,
            interpolate=True,
            label="Capex / FCO",
        )

        plot.set_title(
            "[Capex / FCO] - Bastter", fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel("Capex / FCO %", color="black")
        plot.set_ylim(top=200)
        plot.grid()
        plot.legend()
        plt.show()

    def bastter_capex_fco_flow(self):
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

        plot.plot(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["capex_d_a"],
            color="paleturquoise",
            linestyle="-",
            marker=".",
            markersize=8,
        )

        # Zero mark
        plot.axhline(y=1, color="red", linestyle="--", marker=".", markersize=10)
        plot.axhline(y=3, color="red", linestyle="--", marker=".", markersize=10)

        # Fill Between Profit
        plot.fill_between(
            self.__bastter_full_balance["yr"],
            self.__bastter_full_balance["capex_d_a"],
            where=(self.__bastter_full_balance["capex_d_a"] > 0),
            color="mediumaquamarine",
            alpha=1,
            interpolate=True,
            label="(+) Capex / D&A",
        )

        plot.set_title(
            "[Capex / D&A] - Bastter", fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel("Capex / D&A %", color="black")
        plot.grid()
        plot.legend()
        plt.show()


def main(ticker):
    stock = Plots(ticker)
    stock.bastter_income()
    stock.bastter_capex_fco_flow()


if __name__ == "__main__":
    main("aapl")
