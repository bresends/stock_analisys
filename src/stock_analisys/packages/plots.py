"""
Plot generating Module

"""
import matplotlib.pyplot as plt
import pandas as pd
import stock_analisys.packages.sql_class as sql_class

class Plots:
    def __init__(self, ticker):
        self.ticker = ticker.lower()
        __bastter_obj = sql_class.MySQL('bastter')
        self.__bastter_conn = __bastter_obj.engine
    
    def plot_income(self):
        df = pd.read_sql_table(f'{self.ticker}_full_balance', self.__bastter_conn)
        print(df.head)
        

def main():
    stock = Plots('aapl') 
    stock.plot_income()

if __name__ == "__main__":
    main()