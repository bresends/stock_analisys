"""
Contains the functions related to Transforming HTML content 
For example, converts tables to dataframes
Open HTML files,etc...
"""

from glob import glob
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


def list_files(folder_path):
    """Makes a list with the names of all files in a directory

    Arguments:
        folder_path {path} -- the desired folder 

    Returns:
        [all_files] -- list with the names
    """

    p = Path(rf"{folder_path}").glob("**/*")
    all_files = [str(x.name) for x in p if x.is_file()]
    return all_files


def table_to_pandas(bs4):

    """
    Functions that receives the HTML string from a beautiful soup object
    Returns a Dadaframe with titles
    """

    # Name Extract
    n_columns = 0
    n_rows = 0

    column_names = []

    # Find number of rows and columns / Also Titles

    for row in bs4.find_all("tr"):

        # Determine the number of rows in the table
        td_tags = row.find_all("td")
        if len(td_tags) > 0:
            n_rows += 1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = row.find_all("th")
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0, n_columns)

    df = pd.DataFrame(columns=columns, index=range(0, n_rows))

    row_marker = 0

    for row in bs4.find_all("tr"):
        column_marker = 0
        columns = row.find_all("td")

        for column in columns:
            df.iat[row_marker, column_marker] = column.get_text()
            column_marker += 1

        if len(columns) > 0:
            row_marker += 1

    return df


def main():
    # Tests
    stock = html_file_to_bs4(paths.fundamentei_path / "full_balances" / "AAPL.html")
    print(stock.prettify())


if __name__ == "__main__":

    main()
