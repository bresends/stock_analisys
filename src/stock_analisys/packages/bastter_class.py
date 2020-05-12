"""
File with Bastter Class

It extracts HTML
Sort between REITS and STOCKs
Plot Graphs

"""


# =============================================================================
# Arquivo com as funções relacionadas à classe Bastter
# =============================================================================

import pickle
import random
import time
import webbrowser
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from tabulate import tabulate

# =============================================================================
# Directories Setup
# =============================================================================

cwd_path = Path.cwd()
data_path = cwd_path / 'data'
bin_path = cwd_path / 'bin'


# =============================================================================
# Class Creation
# =============================================================================


class BastterStocks:

    def __init__(self, ticker):

        self.ticker = ticker.upper().strip()
        self.url = f'https://bastter.com/mercado/stock/{ticker}'

    def open_page(self):
        self.driver.get(self.url)

# =============================================================================
# Pega e carrega cookie
# =============================================================================
    def autenticate(self):

        self.driver = webdriver.Chrome(bin_path / 'chromedriver.exe')

        # Puxa os Cookies
        self.driver.get('https://varvy.com/pagespeed/wicked-fast.html')
        self.driver.implicitly_wait(1)

        for cookie in pickle.load(open(bin_path / 'cookies.pkl', "rb")):
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)
        self.print_lines
        print('Cookies Sucessifuly Loaded')


# =============================================================================
# Método de Extração do Company Info
# =============================================================================

    def company_data_extract(self):
        
        """
        Grabs de Company Name, Ticker, Sector and Group from a given company
        Also tells if a given ticker is a REIT or not
        """

        self.driver.get(self.url)

        # Clicando no item (com teste se ele existe)
        teste_company_info = self.driver.find_element_by_xpath(
            '//*[@id="dados-empresa"]')

        # Se está carregado, passa pra frente, senão para.
        if teste_company_info.is_displayed():

            self.driver.find_element_by_xpath(
                '//*[@id="dados-empresa"]/span[2]').click()

        else:

            print('Button not found in page')

        # Extraindo o HTML e gerando o BS4
        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')

        # Dados de STOCKS e REITS JUNTOS

        self.company_name = soup.find('span', class_='ativo-nome').get_text()
        self.sector = soup.find('span', class_='ativo-sector').get_text()

        # Changing United States to USA
        self.company_country = soup.find(
            'span', class_='ativo-inc-country').get_text()

        if self.company_country == ' United States of America':
            self.company_country = 'USA'

        # Condicional de avaliação de REIT

        teste_reit = self.driver.find_element_by_xpath(
            '//*[@id="sidebar-left"]')

        test_bs4 = soup.body.findAll(text='REIT')

        # Se for um REIT:
        if teste_reit.is_displayed() and len(test_bs4) > 0:
            self.sou_um_reit = True
            self.reit_handling()

        # Se for uma STOCK
        else:

            self.sou_um_reit = False
            self.industry_group = soup.find(
                'span', class_='ativo-industry-group').get_text()
            self.industry_category = soup.find(
                'span', class_='ativo-industry-category').get_text()

# =============================================================================
#   Extração da Tabela do HTML
# =============================================================================

    def table_extract(self):

        # Clicando no item (com teste se ele existe)
        teste_selected_data = self.driver.find_element_by_xpath(
            '//*[@id="quadro-simples-menu"]/span[2]')

        # Se está carregado, passa pra frente, senão para.
        if teste_selected_data.is_displayed() == True:

            self.driver.find_element_by_xpath(
                '//*[@id="quadro-simples-menu"]/span[2]').click()
            time.sleep(random.uniform(6, 10))

        else:

            print('Button not found in page')

        # Extraindo o HTML e gerando o BS4
        page_html = self.driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')

        # Extração da Tabela Menor
        simple_balance = soup.find(
            "table", {"class": "evanual quadro table table-striped table-hover marcadagua"})

        # Removendo os valores com percentual
        for span_tag in simple_balance.findAll('span', {'class': 'varperc'}):
            span_tag.replace_with('')

        output_rows = []

        for table_row in simple_balance.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.get_text())
            output_rows.append(output_row)

        # Criação do dataframe a partir da tabela
        self.df_list = pd.DataFrame(output_rows)

        # Transformação dos valore pra string
        self.df_list = self.df_list.applymap(str)

        # Retirada dos pontos e troca das vírgulas pra ponto (pra reconhecimento de decimais)
        self.df_list = self.df_list.applymap(lambda x: x.replace(
            ".", "").replace(",", ".").replace('L', '0').replace('-', '-0'))

        # Retirada de 2 linhas zeradas e uma coluna
        self.df_list = self.df_list.drop([0, 1], axis=0)
        self.df_list = self.df_list.drop([1], axis=1)

        # Nomeação do Header
        df_cols = ['Year', 'Net Revenue', 'Net Income', 'EPS',
                   'EBITDA', 'Net Debt', 'ND/EBITDA', 'FCF', 'FCF/Share']
        self.df_list.columns = df_cols

        # Retorno pra float (pra cálculos)
        self.df_list = self.df_list.applymap(float)

        # Ano pra Int
        self.df_list['Year'] = self.df_list['Year'].apply(int)

        # Põe em Ordem (independente da entrada)
        self.df_list.sort_values(by=['Year'], inplace=True)

# =============================================================================
#  REIT Handling
# =============================================================================

    def reit_handling(self):

        print('')
        self.print_lines()
        print(
            f'-------------- {self.ticker} é um ticker de REIT -------------')
        self.print_lines()
        print('')

        reit_dict = {
            'Ticker': self.ticker,
            'Origin': self.company_country,
            'Company': self.company_name
        }

        # Dataframe de linha única com o Reit

        reit_df = pd.DataFrame.from_dict(reit_dict, orient='index')
        reit_df = reit_df.transpose()

        # Cria um dataframe com as ações já analisadas

        reits_analised = pd.read_csv(data_path / 'bastter_reits.csv')

        df_merge = pd.merge(reit_df, reits_analised, how='outer')

        # Mostra o DF
        print(df_merge.head(1))
        print(df_merge.tail(1))

        # Salva o DF
        df_merge.to_csv(data_path / 'bastter_reits.csv', index=False)
        print('')
        self.print_lines()
        print('-------------- Saved for latter study ------------------ ')
        self.print_lines()

# ======================================================================================
# Função que avalia o percentual de queda ou aumento de um ano pro outro de uma empresa
# ======================================================================================

    def income_percentual(self):

        """
        Function that evaluates drops in revenue year from year
        """

        lista_percentual_lucros = []

        # Pega no DF criado pra cada lista qual o primeiro lucro
        lucro_ano_anterior = self.df_list.iloc[0, 2]

        for lucro_ano in self.df_list['Net Income']:

            # Divide o lucro do ano pelo lucro do ano anterior
            percentual_mudanca = int(
                (lucro_ano - lucro_ano_anterior)/(abs(lucro_ano_anterior + 1))*100)

            # Adiciona na lista
            lista_percentual_lucros.append(percentual_mudanca)

            # Faz com que o valor do ano anterior pego o do ano analisado
            lucro_ano_anterior = (lucro_ano + 0.01)

        self.df_list['%'] = lista_percentual_lucros

        # Prints DF
        print(tabulate(self.df_list, headers='keys', tablefmt='psql'))
        print('')

# =====================================================================================
# Appends a line to a DF with the company data and drops
# =====================================================================================

    def avalicao_stock(self):

        # Contagem dos anos de prejuízo
        anos_prejuizo = [
            item for item in self.df_list['Net Income'] if item <= 0]
        anos_queda_lucro = [item for item in self.df_list['%'] if item < 0]

        stock_info_dict = {
            'Ticker': self.ticker,
            'Origin': self.company_country,
            'Company': self.company_name,
            'Sector': self.sector,
            'Group': self.industry_group,
            'Category': self.industry_category,
            'Loss': len(anos_prejuizo),
            'Income Drop': len(anos_queda_lucro)
        }

        self.df_individual_stock = pd.DataFrame.from_dict(
            stock_info_dict, orient='index')
        self.df_individual_stock = self.df_individual_stock.transpose()

        print(tabulate(self.df_individual_stock, headers='keys', tablefmt='psql'))


    def csv_storage(self):

        """
        Creates a datafram with the analised stocks

        """

        stocks_analisados = pd.read_csv(
            'data/bastter_analysis/bastter_stocks_analised.csv')

        # Faz um merge com o dataframe criado por mim ao analisar a ação
        # Isso tem o intuito de remover duplicatas (o merge junta os iguais)

        df_merge = pd.merge(self.df_individual_stock,
                            stocks_analisados, how='outer')

        print(f'Total of analised companies: [{df_merge.shape[0]}]')
        self.print_lines()

        # Salva o DF com a empresa
        df_merge.to_csv(
            'data/bastter_analysis/bastter_stocks_analised.csv', index=False)

        # Salva os dados da empresa
        self.df_list.to_csv(
            f'data/simplified_balances/{self.ticker} - {self.company_name} - Simple Balance.csv', index=False)
        self.print_lines
        print('Company data sucessefuly stored')


# =============================================================================
# Selenium
# =============================================================================

    def scroll_page_to_table(self):

        table = self.driver.find_element_by_xpath('//*[@id="quadro-simples"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", table)

    def quit_driver(self):
        self.driver.quit()

    def print_lines(self):
        print('--------------------------------------------------------------')


if __name__ == '__main__':
    a = BastterStocks('bby')
    a.autenticate()
    a.company_data_extract()
    a.table_extract()