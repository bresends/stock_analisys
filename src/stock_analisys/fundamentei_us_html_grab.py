import concurrent.futures
import random
import time

import pandas as pd

import stock_analisys.packages.fundamentei_class as fc
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as td


def txt_to_list():
    """Grabs a TXT file and transforms it into a list

    Returns:
        [list] -- [list with all lines from the txt]
    """

    df = pd.read_fwf(paths.fundamentei_path / "all_valid_br_stocks.txt")
    c_to_list = [x for x in df["Ticker"]]
    return c_to_list


def html_grabber(ticker):
    """Steps of actions to Save HTML pages from Fundamentei

    Arguments:
        ticker {[string]} -- [The name of the given company]
    """
    time.sleep(random.uniform(0.1, 0.3))

    stock_obj = fc.FundamenteiExtract(ticker)
    stock_obj.autenticate()
    stock_obj.open_page()
    stock_obj.scroll_page_to_botton()
    stock_obj.html_save()
    stock_obj.driver.quit()


def main():
    """
    Executes Main task of the Module
    In the case receives the list of companies from a function
    Threads in the list to generate the HTML
    """

    tickers_list = txt_to_list()

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        results = executor.map(html_grabber, tickers_list)

    end = time.time()

    td.time_it_secs_conversion(start, end)


if __name__ == "__main__":
    main()
