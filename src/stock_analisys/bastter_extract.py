import concurrent.futures
import pickle
import random
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import stock_analisys.packages.bastter_class as bc
import stock_analisys.packages.html_handling as html_handling
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as prints


def list_fundamentei_stocks():
    files = html_handling.list_files(paths.fundamentei_path / "full_balances_us")
    tickers = list(map(lambda x: x.split(".")[0], files))
    return tickers

def main():
    
    # Receives a list with all possible tickers
    companies_list = list_fundamentei_stocks()
    
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        executor.map(bc.main_extract, companies_list)
    
    end = time.time()

    prints.time_it_secs_conversion(start, end)



if __name__ == "__main__":
    main()
