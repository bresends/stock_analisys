import pandas as pd

import stock_analisys.packages.paths as paths


def csv_to_pd(ticker):
    ticker = ticker.upper().strip()
    df = pd.read_csv(paths.morning_star_path / 'income_statement' / f'{ticker} Income Statement.csv')
    print(df)

def main():
   csv_to_pd('aapl')


if __name__ == "__main__":
    main()
