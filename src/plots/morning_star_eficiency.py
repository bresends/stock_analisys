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
        self.__full_balance = pd.read_sql_table(
            f"{self.ticker}_key_ratios", self.__morning_star_con
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
        self.company_info___full_balance = pd.read_sql_query(
            query, self.__stocks_general_info
        )

    def morning_star_s_g(self):
        """
        Plots Income, r_d and gross_profit for Bastter
        """

        self.pull_basic_info()

        # Setting Fig
        fig = plt.figure()
        fig.set_size_inches(10, 6)

        fig.suptitle(
            f"{self.ticker.upper()} - {self.company_info___full_balance['company_name'][0]}",
            fontsize=14,
            fontweight="bold",
        )

        plot = fig.add_subplot(111)

        # ==========================================================
        # Income & r_d plot
        # ==========================================================

        plot.bar(
            self.__full_balance["yr"],
            self.__full_balance["payables_period"],
            color="steelblue",
            alpha=1,
        )

        plot.plot(
            self.__full_balance["yr"],
            self.__full_balance["payables_period"],
            color="navy",
            alpha=1,
            marker=".",
            label="Payables Period",
        )

        plot.plot(
            self.__full_balance["yr"],
            self.__full_balance["days_inventory"],
            color="deepskyblue",
            marker=".",
            label="Days Inventory",
        )

        plot.plot(
            self.__full_balance["yr"],
            self.__full_balance["day_sales_outstand"],
            color="darkorange",
            marker=".",
            alpha=0.9,
            label="DSO - Day Sales Outstanding",
        )

        plot.set_title(
            "Eficiency Days - Morning Star", fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel("Eficiency Days", color="black")
        plot.grid()
        plot.legend()
        plt.show()


def main(ticker):
    stock = Plots(ticker)
    stock.morning_star_s_g()


if __name__ == "__main__":
    main("aapl")
