"""
Dumps the CSV with Fundamentei Financials to MySQL 
"""
import concurrent.futures
import random
import time

import pandas as pd
import sqlalchemy

import stock_analisys.packages.paths as paths
from stock_analisys.packages.fundamentei_class import main_evaluate
from stock_analisys.packages.prints import time_it
from stock_analisys.packages.sql_class import MySQL


def full_financials(ticker):

    """
    Alter the Morning Star Tables to dump it to MySQL
    """

    ticker = ticker.upper().strip()
    print(ticker)

    ms_sql = MySQL(database="fundamentei")
    table_name = f"{ticker}_full_balance"

    # Pull DF from FundamenteiClass
    df = main_evaluate(ticker)

    # Filtering Banks and regular companies
    try:
        df["Net Inc."]
    except KeyError:

        print(f"{ticker} is a Bank")

        df = df.rename(columns={"Net Income": "Net Inc."})
        df["EBITDA"] = 0
        df["EBIT"] = 0
        df["D&A"] = 0
        df["Cash"] = 0
        df["Debt"] = 0
        df["N.D. / EBITDA"] = 0
        df["OCF"] = 0
        df["CAPEX"] = 0
        df["FCF"] = 0
        df["Free"] = 0

    # Filtering Companies without ROE
    try:
        df["ROE"]
    except KeyError:

        print(f"{ticker} No ROE Company")

        df = df.rename(columns={"Net Income": "Net Inc."})
        df["ROE"] = 0

    # Filtering Companies without Payout
    try:
        df["Payout"]
    except KeyError:

        print(f"{ticker} No ROE Company")

        df = df.rename(columns={"Net Income": "Net Inc."})
        df["Payout"] = 0

    # Filtering just the important columns
    df = df.loc[
        :,
        [
            "Year",
            "Equity",
            "Revenue",
            "EBITDA",
            "EBIT",
            "D&A",
            "Net Inc.",
            "%",
            "Net Mar.",
            "ROE",
            "Cash",
            "Debt",
            "N.D. / EBITDA",
            "OCF",
            "CAPEX",
            "FCF",
            "Free",
            "Payout",
        ],
    ]

    # Fixing names
    df = df.rename(
        columns={
            "Year": "yr",
            "Equity": "equity",
            "Revenue": "revenue",
            "EBITDA": "ebitda",
            "EBIT": "ebit",
            "D&A": "d_a",
            "Net Inc.": "net_income",
            "%": "var_net_inc",
            "Net Mar.": "net_margin",
            "ROE": "roe",
            "Cash": "cash",
            "Debt": "debt",
            "N.D. / EBITDA": "nd_ebitda",
            "OCF": "ocf",
            "CAPEX": "capex",
            "FCF": "fin_cf",
            "Free": "fcf",
            "Payout": "payout",
        }
    )

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
            "ebitda": sqlalchemy.types.INTEGER(),
            "ebit": sqlalchemy.types.INTEGER(),
            "d_a": sqlalchemy.types.INTEGER(),
            "net_income": sqlalchemy.types.INTEGER(),
            "net_margin": sqlalchemy.types.INTEGER(),
            "roe": sqlalchemy.types.INTEGER(),
            "cash": sqlalchemy.types.INTEGER(),
            "debt": sqlalchemy.types.INTEGER(),
            "nd_ebitda": sqlalchemy.types.INTEGER(),
            "ocf": sqlalchemy.types.INTEGER(),
            "capex": sqlalchemy.types.INTEGER(),
            "fin_cf": sqlalchemy.types.INTEGER(),
            "fcf": sqlalchemy.types.INTEGER(),
            "payout": sqlalchemy.types.INTEGER(),
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
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        executor.map(main, ticker_list)


if __name__ == "__main__":
    # main("jpm")
    main_all_tickers()
    # main_concurrent()
