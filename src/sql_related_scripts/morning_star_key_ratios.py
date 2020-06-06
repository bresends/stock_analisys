"""
Dumps the CSV with Morning Star Financials to MySQL 
"""
import concurrent.futures
import random
import time

import pandas as pd

import stock_analisys.packages.paths as paths
from stock_analisys.packages.prints import time_it
from stock_analisys.packages.sql_class import MySQL


def key_ratios_to_sql(ticker):

    """
    Alter the Morning Star Tables to dump it to MySQL
    """

    ticker = ticker.upper().strip()

    ms_sql = MySQL(database="morning_star")
    table_name = f"{ticker}_key_ratios"

    def create_table():
        querry = f""" \
        CREATE TABLE IF NOT EXISTS {table_name}( \
        yr INT PRIMARY KEY NOT NULL, \
        revenue INT NOT NULL, \
        operating_income INT NOT NULL, \
        net_income INT NOT NULL, \
        eps FLOAT(2) NOT NULL, \
        payout FLOAT(2) NOT NULL DEFAULT 0 ,\
        debt_equity FLOAT(2) DEFAULT 0 ,\
        interest_coverage FLOAT(2) NOT NULL, \
        ocs INT NOT NULL, \
        fcf INT NOT NULL, \
        gross_margin FLOAT(2) DEFAULT 0 ,\
        operating_margin FLOAT(2) DEFAULT 0 ,\
        net_margin FLOAT(2) DEFAULT 0 ,\
        cogs_perc FLOAT(2) NOT NULL, \
        sga_perc FLOAT(2) NOT NULL, \
        r_d_perc FLOAT(2) NOT NULL, \
        fin_leverage FLOAT(2) NOT NULL, \
        day_sales_outstand FLOAT(2) NOT NULL, \
        days_inventory FLOAT(2) NOT NULL, \
        payables_period INT NOT NULL, \
        cash_conversion_cicle FLOAT(2) NOT NULL, \
        receivables_turnover FLOAT(2) NOT NULL, \
        inventory_turnover FLOAT(2) NOT NULL, \
        assests_turnover FLOAT(2) NOT NULL, \
        shares INT NOT NULL, \
        var_revenue FLOAT(2) DEFAULT 0 ,\
        var_operating_inc FLOAT(2) DEFAULT 0 ,\
        var_net_inc FLOAT(2) DEFAULT 0 ,\
        var_eps FLOAT(2) DEFAULT 0 ); \
        """
        ms_sql.engine.execute(querry)

        print(f"Creating table {ticker}_key_ratios")

    create_table()

    # Dataframe part of function
    df = pd.read_csv(
        paths.morning_star_path / "key_ratios" / f"{ticker} Key Ratios.csv",
        decimal=",",
    )
    df = df.transpose()
    df = df.reset_index()

    # Fixing Header
    new_header = df.iloc[0]
    df = df[1:]  # Discards 0 row
    df.columns = new_header
    df.columns.values[0] = "yr"

    # Filling NaN
    df = df.fillna(0)

    # Fixing Types
    df = df.applymap(str)
    df = df.applymap(lambda x: x.replace(",", ""))
    df["yr"] = df["yr"].apply(lambda x: int(x.replace("TTM", "2020").split("-")[0]))

    # Filtering just the important columns
    df = df.loc[
        :,
        [
            "yr",
            "Revenue USD Mil",
            "Operating Income USD Mil",
            "Net Income USD Mil",
            "Earnings Per Share USD",
            "Payout Ratio % *",
            "Debt/Equity",
            "Interest Coverage",
            "Operating Cash Flow USD Mil",
            "Free Cash Flow USD Mil",
            "Gross Margin %",
            "Operating Margin %",
            "Net Margin %",
            "COGS",
            "SG&A",
            "R&D",
            "Financial Leverage (Average)",
            "Days Sales Outstanding",
            "Days Inventory",
            "Payables Period",
            "Cash Conversion Cycle",
            "Receivables Turnover",
            "Inventory Turnover",
            "Asset Turnover",
            "Shares Mil",
            "Year over Year",
        ],
    ]

    # Fixing names
    df = df.rename(
        columns={
            "Revenue USD Mil": "revenue",
            "Operating Income USD Mil": "operating_income",
            "Net Income USD Mil": "net_income",
            "Earnings Per Share USD": "eps",
            "Payout Ratio % *": "payout",
            "Debt/Equity": "debt_equity",
            "Interest Coverage": "interest_coverage",
            "Operating Cash Flow USD Mil": "ops",
            "Free Cash Flow USD Mil": "fcf",
            "Gross Margin %": "gross_margin",
            "Operating Margin %": "operating_margin",
            "Net Margin %": "net_margin",
            "COGS": "cogs_perc",
            "SG&A": "sga_perc",
            "R&D": "r_d_perc",
            "Financial Leverage (Average)": "fin_leverage",
            "Days Sales Outstanding": "day_sales_outstand",
            "Days Inventory": "days_inventory",
            "Payables Period": "payables_period",
            "Cash Conversion Cycle": "cash_conversion_cicle",
            "Receivables Turnover": "receivables_turnover",
            "Inventory Turnover": "inventory_turnover",
            "Asset Turnover": "assests_turnover",
            "Shares Mil": "shares",
        }
    )

    # Fixing Last Names
    cols = list(df.columns)
    cols[-4] = "var_revenue"
    cols[-3] = "var_operating_inc"
    cols[-2] = "var_net_inc"
    cols[-1] = "var_eps"

    df.columns = cols

    # Types convertion
    df["revenue"] = df["revenue"].astype("int")
    df["operating_income"] = df["operating_income"].astype("int")
    df["net_income"] = df["net_income"].astype("int")
    df["eps"] = df["eps"].astype("float")
    df["payout"] = df["payout"].astype("float")
    df["debt_equity"] = df["debt_equity"].astype("float")
    df["interest_coverage"] = df["interest_coverage"].astype("float")
    df["ops"] = df["ops"].astype("int")
    df["fcf"] = df["fcf"].astype("int")
    df["gross_margin"] = df["gross_margin"].astype("float")
    df["operating_margin"] = df["operating_margin"].astype("float")
    df["net_margin"] = df["net_margin"].astype("float")
    df["cogs_perc"] = df["cogs_perc"].astype("float")
    df["sga_perc"] = df["sga_perc"].astype("float")
    df["r_d_perc"] = df["r_d_perc"].astype("float")
    df["fin_leverage"] = df["fin_leverage"].astype("float")
    df["day_sales_outstand"] = df["day_sales_outstand"].astype("float")
    df["days_inventory"] = df["days_inventory"].astype("float")
    df["payables_period"] = df["payables_period"].astype("float")
    df["cash_conversion_cicle"] = df["cash_conversion_cicle"].astype("float")
    df["receivables_turnover"] = df["receivables_turnover"].astype("float")
    df["inventory_turnover"] = df["inventory_turnover"].astype("float")
    df["assests_turnover"] = df["assests_turnover"].astype("float")
    df["shares"] = df["shares"].astype("int")
    df["var_revenue"] = df["var_revenue"].astype("float")
    df["var_operating_inc"] = df["var_operating_inc"].astype("float")
    df["var_net_inc"] = df["var_net_inc"].astype("float")
    df["var_eps"] = df["var_eps"].astype("float")
    

    print(df)

    # Dump DQL Part
    df.to_sql(
        name=table_name.lower(),  # database table name
        con=ms_sql.engine,
        if_exists="replace",
        index=False,
    )

    print("Sucessifuly Saved to MySQL")
    print(
        "------------------------------------------------------------------------------------------------"
    )


def main(ticker):
    time.sleep(random.uniform(0.1, 1))
    key_ratios_to_sql(ticker)


@time_it
def main_concurrent():
    df = pd.read_csv("good_stocks.csv")
    ticker_list = [x for x in df["Ticker"]]
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        executor.map(main, ticker_list)


if __name__ == "__main__":
    # main("aapl")
    main_concurrent()
