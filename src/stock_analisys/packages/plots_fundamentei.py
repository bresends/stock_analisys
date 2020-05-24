"""
Tentativa de uso do seaborn pra plotagem dos gráficos
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import stock_analisys.packages.fundamentei_class as fc


def fundamentei_plot(df, company_obj):

    fig = plt.figure()
    fig.set_size_inches(30, 12)
    fig.suptitle(
        f"{company_obj.ticker} - {company_obj.name}", fontsize=14, fontweight="bold"
    )

    company_info = fig.add_subplot(131)
    profits_graph = fig.add_subplot(132)
    nd_ebitda = fig.add_subplot(133)

    # ==========================================================
    # Infos plot
    # ==========================================================

    company_info.set_axis_off()
    company_info.set_aspect("auto", anchor="W")

    def write_text(text="Teste", x=0, y=0, size_font=12, alignment="left"):

        company_info.text(
            x,
            y,
            text,
            horizontalalignment=alignment,
            bbox=dict(facecolor="gray", alpha=0.05, pad=1, edgecolor="none"),
            transform=company_info.transAxes,
            fontsize=size_font,
            wrap=True,
        )

    write_text(f"Company: {company_obj.name}", 0.5, 1, 18, "center")

    write_text(f"Fundation: {company_obj.fundation}", 0, 0.9)
    write_text(f"IPO: {company_obj.ipo}", 0, 0.85)
    write_text(f"Industry: {company_obj.industry}", 0, 0.80)
    write_text(f"Market Cap: {company_obj.market_cap}", 0, 0.75)

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

    plt.subplots_adjust(
        left=0.02, bottom=0.2, right=0.98, top=0.87, wspace=0.16, hspace=0.2
    )
    plt.show()

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
    fundamentei_plot(dataframe, company)

    # Print Description
    print(company.description)

if __name__ == "__main__":
    main('aapl')
    
