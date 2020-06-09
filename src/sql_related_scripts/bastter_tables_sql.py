"""
Dumps the CSV with Fundamentei Financials to MySQL 
"""
import concurrent.futures
import random
import time

import numpy as np
import pandas as pd
import sqlalchemy

import stock_analisys.packages.paths as paths
from stock_analisys.packages.bastter_class import main_evaluate
from stock_analisys.packages.prints import time_it
from stock_analisys.packages.sql_class import MySQL


def full_financials(ticker):

    """
    Alter the Morning Star Tables to dump it to MySQL
    """

    ticker = ticker.upper().strip()
    print(ticker)

    ms_sql = MySQL(database="bastter")
    table_name = f"{ticker}_full_balance"

    # Pull DF from FundamenteiClass
    df = main_evaluate(ticker)

    # Filtering just the important columns
    df = df.loc[
        :,
        [
            "Year",
            "Equity",
            "Net Revenue",
            "Operating Income",
            "Net Income",
            "%-Net Income",
            "Earnings per Share",
            r"%-Earnings per Share",
            "EBIT",
            "EBITDA",
            "EBITDA Margin",
            "OIBDA",
            "OIBDA Margin",
            "Depreciation and Amortization",
            "Net Debt",
            "Net Debt / EBITDA",
            "Net Profit Margin",
            "Net Debt/Equity",
            "ROE",
            "Cash",
            "Debt",
            "Operating Activities",
            "Investing",
            "Capital Expenditures (CAPEX)",
            "FCF",
            "Financing",
            "FCF/OCF",
            "Total",
            "Payout",
        ],
    ]

    # Fixing names
    df = df.rename(
        columns={
            "Year": "yr",
            "Equity": "equity",
            "Net Revenue": "revenue",
            "Operating Income": "operating_income",
            "Net Income": "net_income",
            "%-Net Income": "var_net_inc",
            "Earnings per Share": "eps",
            r"%-Earnings per Share": "var_eps",
            "EBIT": "ebit",
            "EBITDA": "ebitda",
            "EBITDA Margin": "ebitda_margin",
            "OIBDA": "oibda",
            "OIBDA Margin": "oibda_margin",
            "Depreciation and Amortization": "d_a",
            "Net Debt": "net_debt",
            "Net Debt / EBITDA": "nd_ebitda",
            "Net Profit Margin": "net_margin",
            "Net Debt/Equity": "debt_equity",
            "ROE": "roe",
            "Cash": "cash",
            "Debt": "debt",
            "Operating Activities": "ocf",
            "Investing": "investing",
            "Capital Expenditures (CAPEX)": "capex",
            "FCF": "fcf",
            "Financing": "fin_cash_flow",
            "FCF/OCF": "fcf_ocf",
            "Total": "total",
            "Payout": "payout",
        }
    )

    # # Fix zeros
    # if 0 in df["d_a"]:
    #     df["d_a"] = df["d_a"] + 1

    # if 0 in df["d_a"]:
    #     df["ocf"] = df["ocf"] + 1

    df["capex_fco"] = abs(round(((df["capex"] / df["ocf"]) * 100), 2))
    df["capex_d_a"] = abs(round(((df["capex"] / df["d_a"]) * 1), 2))

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)

    print(df)

    # Dump DQL Part
    df.to_sql(
        name=table_name.lower(),  # database table name
        con=ms_sql.engine,
        if_exists="replace",
        index=False,
        dtype={
            "equity": sqlalchemy.types.INTEGER(),
            "revenue": sqlalchemy.types.INTEGER(),
            "operating_income": sqlalchemy.types.INTEGER(),
            "net_income": sqlalchemy.types.INTEGER(),
            "var_net_inc": sqlalchemy.types.INTEGER(),
            "eps": sqlalchemy.types.FLOAT(precision=2),
            "var_eps": sqlalchemy.types.INTEGER(),
            "ebit": sqlalchemy.types.INTEGER(),
            "ebitda": sqlalchemy.types.INTEGER(),
            "ebitda_margin": sqlalchemy.types.INTEGER(),
            "oibda": sqlalchemy.types.INTEGER(),
            "oibda_margin": sqlalchemy.types.INTEGER(),
            "d_a": sqlalchemy.types.INTEGER(),
            "net_debt": sqlalchemy.types.INTEGER(),
            "nd_ebitda": sqlalchemy.types.FLOAT(precision=2),
            "net_margin": sqlalchemy.types.INTEGER(),
            "debt_equity": sqlalchemy.types.FLOAT(precision=2),
            "roe": sqlalchemy.types.INTEGER(),
            "cash": sqlalchemy.types.INTEGER(),
            "debt": sqlalchemy.types.INTEGER(),
            "ocf": sqlalchemy.types.INTEGER(),
            "investing": sqlalchemy.types.INTEGER(),
            "capex": sqlalchemy.types.INTEGER(),
            "fcf": sqlalchemy.types.INTEGER(),
            "fin_cash_flow": sqlalchemy.types.INTEGER(),
            "fcf_ocf": sqlalchemy.types.FLOAT(precision=2),
            "total": sqlalchemy.types.INTEGER(),
            "payout": sqlalchemy.types.FLOAT(precision=2),
            "capex_fco": sqlalchemy.types.FLOAT(precision=2),
            "capex_d_a": sqlalchemy.types.FLOAT(precision=2),
        },
    )

    print("Sucessifuly Saved to MySQL")
    print(
        "------------------------------------------------------------------------------------------------"
    )


def main(ticker):
    time.sleep(random.uniform(0.1, 1))
    full_financials(ticker)


@time_it
def main_all_tickers():
    df = pd.read_csv("good_stocks.csv")
    for item in df["Ticker"]:
        main(item)


@time_it
def main_concurrent():
    df = pd.read_csv("good_stocks.csv")
    ticker_list = [x for x in df["Ticker"]]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(main, ticker_list)


if __name__ == "__main__":
    # main("trow")
    main_all_tickers()
    # main_concurrent()
