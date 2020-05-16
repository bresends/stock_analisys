from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

import stock_analisys.packages.paths as paths


# =============================================================================
# Functions
# =============================================================================


def html_file_to_bs4(chosen_file):

    """ 
    Receives a file path and retrives the HTML file from it. 
    """
    with open(chosen_file, "r", encoding="utf-8") as f:
        html_result = BeautifulSoup(f, "lxml")

    return html_result


def main():
    """
    Tests 
    """

    stock = html_open(paths.fundamentei_path / 'full_balances' /"AAPL.html")
    print(stock.prettify())


if __name__ == "__main__":

    main()
