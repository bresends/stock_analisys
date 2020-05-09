# -*- coding: utf-8 -*-
"""
Arquivo usado pra usar minhas funções
"""

# Importação dos Módulos Externos

import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

"""
-------------------------------------------------------------------------------
Função Base
Nesse caso uma função que recebe uma URL e devolve um Bs4
-------------------------------------------------------------------------------
"""
    
def url_bs4(url):

    # Formando o Header 
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
        
    # Testando a URL 
    try:
        print(f'Analisando a página {url}')
        page = requests.get(url, headers = header, timeout=5)
        
        # Se a página carregou mas não deu 200 mostra o erro e Fala que o Soup é Falso
        if page.status_code != 200:
            print(f'A requisição da página {url} retornou o erro {page.status_code}')
            soup = False
            
        # Se o retorno foi 200, cria o BS4
        else:
            soup = BeautifulSoup(page.text, 'lxml')
            print(f' BS4 criado com sucesso')
            
    except Exception as erro:
        print(f'Ao tentar pegar a URL tivemos o erro [{erro}]')
        soup = False
    
    # Descansa 1 segundo entre as calls         
    time.sleep(5)
    
    return soup

"""
-------------------------------------------------------------------------------
Função de Paralelização 
-------------------------------------------------------------------------------
"""
   
def main(lista_links):
    
    
    # Criando uma função que vai Criar o Pool de trabalhadores 
    with ThreadPoolExecutor(max_workers=3) as executor:
        
        """ Criamos um grupo de trabalho(futures) para cada um dos trabalhadores com uma 'list comprehension'"""
        # É como se eu tivesse feito 
        future_to_url = [executor.submit(url_bs4, url) for url in lista_links]
        
        """Essa parte do programa faz o seguinte: 
        O as_completed é uma função que captura "O RETORNO DA FUNÇÃO" de cada um do trabalhadores medida que eles completam
        Mas isso não devolve uma lista como no map e sim um interador que precisa ser passado pr aoutra coisa. 
        Assim que eles todos terminam, faz o que quiser com o resultado retornado pela função aplicada"""
        
        for item in as_completed(future_to_url):
            try:                     
                retornos_futuros = item.result() # Não pode esquecer o .result, senão ele fica um Objeto Futures
                
                # Testa o conteúdo dos resultados
                if retornos_futuros != None:
                    stocks_info.append(retornos_futuros)
                else:
                    stocks_info.append(0)
            
            except Exception as erro:
                print(f'Essa iteração específica da função não foi possível. Erro {erro}')
            
    # Retorna a lista com os resultados das puxadas BS4 paralelas 
    return stocks_info 
            



if __name__ == '__main__':
    
    # Lista onde as informações serão armazenadas
    
    stocks_info = []
    
    # Faço uma lista com os links a serem avaliados
    links = ['https://www.google.com/search?q=aaho+stock','https://www.google.com/search?q=bb+stock', 'https://www.google.com/search?q=cc+stock']
    
    # Executo a Função Main jogando como parametro a lista Links 
    main(links)
    
    # Mostra o Return da main 
    for item in stocks_info:
        print(item.h2.get_text())

    

    
    
    

