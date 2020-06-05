"""
Dumps the CSV with Morning Star Financials to MySQL 
"""
import pandas as pd

import stock_analisys.packages.paths as paths
from stock_analisys.packages.sql_class import MySQL


def income_statement_to_my_sql(ticker):

    """
    Alter the Morning Star Tables to dump it to MySQL
    """

    ticker = ticker.upper().strip()

    ms_sql = MySQL(database="morning_star")
    table_name = f"{ticker}_financial"

    def create_table():
        querry = f""" \
        CREATE TABLE IF NOT EXISTS {table_name}( \
        yr INT PRIMARY KEY NOT NULL, \
        revenue INT NOT NULL, \
        cost_of_revenue INT NOT NULL, \
        gross_profit INT NOT NULL, \
        r_d INT DEFAULT 0, \
        s_g INT NOT NULL, \
        operating_income INT NOT NULL, \
        s_g_gross_profit FLOAT(2) NOT NULL,
        r_d_gross_profit FLOAT(2) DEFAULT 0); \
        """
        ms_sql.engine.execute(querry)

        print(f"Creating table {ticker}_financial")

    create_table()

    # Dataframe part of function
    df = pd.read_csv(
        paths.morning_star_path / "income_statement" / f"{ticker} Income Statement.csv"
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
    df["yr"] = df["yr"].apply(lambda x: int(x.replace("TTM", "2020").split("-")[0]))
    df = df.applymap(int)

    try:
        df["Research and development"]

    except KeyError:
        df["Research and development"] = 0

    # Filtering just the important columns
    df = df.loc[
        :,
        [
            "yr",
            "Revenue",
            "Cost of revenue",
            "Gross profit",
            "Research and development",
            "Sales, General and administrative",
            "Operating income",
        ],
    ]

    df = df.rename(
        columns={
            "Revenue": "revenue",
            "Cost of revenue": "cost_of_revenue",
            "Gross profit": "gross_profit",
            "Research and development": "r_d",
            "Sales, General and administrative": "s_g",
            "Operating income": "operating_income",
        }
    )

    # Creating Extra columns

    df["s_g_gross_profit"] = round(((df["s_g"] / df["gross_profit"]) * 100), 2)
    df["r_d_gross_profit"] = round(((df["r_d"] / df["gross_profit"]) * 100), 2)

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
    income_statement_to_my_sql(ticker)


if __name__ == "__main__":

    df = pd.read_csv("test.csv")
    for item in df["Ticker"]:
        main(item)
