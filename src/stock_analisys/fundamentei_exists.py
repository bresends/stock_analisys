"""
Program with task of utilizing the Fundamentei Object
From a list os stocks check if the given ticker exists or not in the Fundamentei Site
"""

import concurrent.futures
import random
import time

import pandas as pd

import stock_analisys.packages.fundamentei_class as fc
import stock_analisys.packages.paths as paths
import stock_analisys.packages.prints as prints


def df_to_list():
    df = pd.read_csv(paths.data_path / "original_lists" / "all_us_tickers.csv")
    c_to_list = [x for x in df["Ticker"]]
    return c_to_list


def evaluate(ticker):
    time.sleep(random.uniform(0.1, 1))
    existence_test = fc.FundamenteiEvaluate(ticker)
    existence_test.evaluate_existence()
    time.sleep(random.uniform(0.5, 1))


def main():
    """
    Executes Main task of the Module
    In the case receives the list of companies from a function
    Threads in the list to generate the txt with the valid ones
    """
    
    companies_list = df_to_list()
    
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        # Start the load operations and mark each future with its URL
        results = executor.map(evaluate, companies_list)
    
    end = time.time()

    prints.time_it_secs_conversion(start, end)




if __name__ == "__main__":
    main()
