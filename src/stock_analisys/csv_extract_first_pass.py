"""
File that save CSVs from companies in the original 4K csv bastter list
Make use of BastterStocks module (it is a class)

"""
import time
import random
import pandas as pd
import webbrowser
import concurrent.futures


def main(index):
    """
    Grabs de CSV files for all the 4700 stocks in Bastter Site
    """
    # Time for avoiding conflicts between passes
    time.sleep(random.uniform(0.1, 10))

    # Stock Selection
    csv_stocks_original = pd.read_csv(
        'data/listas_originais/[4K] - bastter_original.csv')

    stock_pick = csv_stocks_original.loc[index, 'Ticker']
    print('--------------------------------------------------------------------------------------')
    print(f'Saving: {stock_pick}')
    print('--------------------------------------------------------------------------------------')

    # Object Instanciate
    stock = BastterStocks(stock_pick)

    # Methods
    try:
        stock.autenticate()
        stock.company_data_extract()

        # Definição da utilização ou não do resto das funções se for um REIT ou Stock
        if stock.sou_um_reit == True:

            print('')

        else:

            stock.table_extract()
            stock.scroll_page_to_table()
            stock.income_percentual()
            stock.avalicao_stock()
            stock.csv_storage()

    # Erro do TTM na Tabela
    except ValueError as erro:

        print(stock.ticker)
        print(type(erro))
        print(erro.args)
        print(erro)

    except Exception as erro:
        print(stock.ticker)
        print(type(erro))
        print(erro.args)
        print(erro)

    finally:
        stock.quit_driver()


if __name__ == '__main__':

    companies = range(0, 500)  # Repetir
    inicio = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        results = executor.map(main, companies)

    fim = time.time()

    tempo_gasto = fim - inicio

    if tempo_gasto < 60:
        print('----------------------------------------------------')
        print(f'Time spent in execution = {tempo_gasto} seconds')
        print('----------  Done ---------------')
    else:
        tempo_minutos = tempo_gasto/60
        print('----------------------------------------------------')
        print(f'Time spent in execution = {tempo_minutos} minutes')
        print('----------  Done ---------------')
