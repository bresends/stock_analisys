""" 
    Programa to generate the data for the yellow and red stocks for bastter (also the new companies)

"""

import pandas as pd
from pathlib import Path

"""
Path Set
"""

cwd_path = Path.cwd()
data_path = cwd_path / "data"
bin_path = cwd_path / "bin"

# Funtions


def open_file():
    df_yellow_tickers = pd.read_csv(data_path / 'bastter_analysis' / 'bastter_yellow.csv' )
    return df_yellow_tickers


def analyse(df, index):
    company = df.iloc[index, 0]
    return company


if __name__ == "__main__":
    df = open_file()
    result = analyse(df, 0)

    print(f"Analising the Company: {result}")

    stock_object = br.Company(result)

    # Methods
    stock_object.data_retrieve()
    stock_object.data_info_to_clipboard()
    stock_object.plot_income()
