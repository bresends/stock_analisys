import concurrent.futures
import random
import time
import pickle

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import stock_analisys.packages.bastter_class as bc
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as prints


def df_to_list():
    df = pd.read_csv(paths.data_path / "original_lists" / "all_us_tickers.csv")
    c_to_list = [x for x in df["Ticker"]]
    return c_to_list

def main():
    
    # Receives a list with all possible tickers
    companies_list = df_to_list()
    
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        # Start the load operations and mark each future with its URL
        results = executor.map(bc.main_extract, companies_list)
    
    end = time.time()

    prints.time_it_secs_conversion(start, end)



if __name__ == "__main__":
    main()
