"""
Tentativa de uso do seaborn pra plotagem dos gráficos
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import stock_analisys.packages.fundamentei_class as fc


def fundamentei_profit_debt_plot(df, company_obj):

    fig = plt.figure()
    fig.set_size_inches(12, 5)
    fig.suptitle(
        f"{company_obj.ticker} - {company_obj.name}", fontsize=14, fontweight="bold"
    )

    profits_graph = fig.add_subplot(121)
    nd_ebitda = fig.add_subplot(122)

    # ==========================================================
    # Income & EBIT plot
    # ==========================================================
    profits_graph.bar(df["Year"], df["EBIT"], color="orange", alpha=0.8, label="EBIT")

    profits_graph.plot(
        df["Year"],
        df["Net Inc."],
        color="green",
        linestyle="-",
        marker=".",
        markersize=8,
    )

    # Zero mark
    profits_graph.axhline(color="red", linestyle="--", marker=".", markersize=10)

    # Fill Between Profit
    profits_graph.fill_between(
        df["Year"],
        df["Net Inc."],
        where=(df["Net Inc."] > 0),
        color="g",
        alpha=1,
        interpolate=True,
        label="Profit",
    )

    # Fill Between Loss
    profits_graph.fill_between(
        df["Year"],
        df["Net Inc."],
        where=(df["Net Inc."] < 0),
        color="r",
        alpha=0.95,
        interpolate=True,
        label="Loss",
    )

    profits_graph.set_title(
        "[Net Income]", fontsize=12, color="black",
    )

    profits_graph.set_xlabel("Year", color="black")
    profits_graph.set_ylabel("Net Income (mil)", color="black")
    profits_graph.grid()
    profits_graph.legend()

    # ==========================================================
    # ND/Ebitda Plot
    # ==========================================================

    nd_ebitda.plot(
        df["Year"],
        df["N.D. / EBITDA"],
        color="blue",
        linestyle="-",
        marker=".",
        markersize=8,
    )

    # Control line for debt
    nd_ebitda.axhline(y=3, color="red", linestyle="--", marker=".", markersize=10)

    # Fill Debt
    nd_ebitda.fill_between(
        df["Year"],
        df["N.D. / EBITDA"],
        y2=3,
        where=(df["N.D. / EBITDA"] < 3),
        color="b",
        alpha=0.6,
        interpolate=True,
        label="Debt Free",
    )

    nd_ebitda.fill_between(
        df["Year"],
        df["N.D. / EBITDA"],
        y2=3,
        where=(df["N.D. / EBITDA"] > 3),
        color="r",
        alpha=0.8,
        interpolate=True,
        label="Debt",
    )

    nd_ebitda.set_title(
        "[Debt/EBITDA]", fontdict={"fontsize": 12}, color="black",
    )

    nd_ebitda.set_xlabel("Year", color="black")
    nd_ebitda.set_ylabel("ND / EBITDA (mil)", color="black")
    nd_ebitda.grid()
    nd_ebitda.legend()

    # plt.subplot_tool()

    plt.tight_layout()
    plt.show()

    # ===========================================================================
    # FIG 2 - Margin & Profit
    # ===========================================================================

    fig2 = plt.figure()
    fig2.set_size_inches(12, 5)

    net_margin = fig2.add_subplot(121)
    payout = fig2.add_subplot(122)

    net_margin.plot(
        df["Year"],
        df["Net Mar."],
        color="red",
        linestyle="-",
        marker=".",
        markersize=8,
    )

    # Zero mark
    net_margin.axhline(y=20, color="red", linestyle="--", marker=".", markersize=10)

    # Fill Between Loss
    net_margin.fill_between(
        df["Year"],
        df["Net Mar."],
        y2=20,
        where=(df["Net Mar."] < 20),
        color="r",
        alpha=0.75,
        interpolate=True,
        label="Less than Ideal",
    )

    # Fill Between Loss
    net_margin.fill_between(
        df["Year"],
        df["Net Inc."],
        y2=20,
        where=(df["Net Mar."] > 20),
        color="b",
        alpha=0.75,
        interpolate=True,
        label=" Ideal",
    )

    net_margin.set_title(
        "[Net Mar.]", fontsize=12, color="black",
    )

    net_margin.set_xlabel("Year", color="black")
    net_margin.set_ylabel("Net Mar. (%)", color="black")
    net_margin.grid()
    net_margin.legend()

    # Payout

    try:

        # Zero mark
        payout.axhline(y=10, color="green", linestyle="--", marker=".", markersize=10)
        payout.axhline(
            y=25, color="darkorange", linestyle="--", marker=".", markersize=10
        )
        payout.axhline(y=50, color="red", linestyle="--", marker=".", markersize=10)

        payout.plot(
            df["Year"],
            df["Payout"],
            color="magenta",
            linestyle="-",
            marker=".",
            markersize=8,
        )

        payout.bar(df["Year"], df["Payout"], color="pink", label="Payout")

        payout.set_title(
            "[Payout]", fontsize=12, color="black",
        )

        payout.set_xlabel("Year", color="black")
        payout.set_ylabel("Payout(%)", color="black")
        payout.grid()
        payout.legend()

        plt.tight_layout()
        plt.show()
    except:
        print("No payout")


def main(ticker):

    # Instanciate Objetct
    company = fc.FundamenteiEvaluate(ticker)

    # Grabs Stock Financial Data
    company.table_extract()
    company.income_percentual()

    # Grabs Stock General Info
    company.company_informations()

    # Plots
    dataframe = company.company_full_data
    fundamentei_profit_debt_plot(dataframe, company)


if __name__ == "__main__":
    main("aapl")
