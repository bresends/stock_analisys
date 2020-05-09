import pandas as pd
from tabulate import tabulate

def print_dataframe(df):
    """
    Printa os valores no Dataframe 
    """
    print(tabulate(df, headers='keys', tablefmt='pqsl'))