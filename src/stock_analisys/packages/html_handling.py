from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


# =============================================================================
# Functions
# =============================================================================


def html_open(chosen_file):

    """ 
    Receives a file and retrives the HTML file from it. 
    """
    with open(chosen_file, "r", encoding="utf-8") as f:
        html_result = BeautifulSoup(f, "lxml")

    return html_result


def main():

    stock = html_open(fundamentei_balances / "AAPL.html")
    print(stock.prettify())


if __name__ == "__main__":

    main()
