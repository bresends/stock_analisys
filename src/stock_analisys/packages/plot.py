"""
Plot generating Module
It prints the Income and Debt Graphs for the user. 

"""
import pandas as pd
import matplotlib.pyplot as plt

def graf_income_debt(df, ticker, company_name):
        
        # Coordenadas de Plotagem da linha de controle de ambos os gráficos
    
        x_cordinates = [df['Year'].iloc[0], df['Year'].iloc[-1]]
        y_cordinates = [0,0]
        
        x2_cordinates = [df['Year'].iloc[0], df['Year'].iloc[-1]]
        y2_cordinates = [3,3]
        
        
        # Definição do subplot
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))
        
        #Define a função que vai plotar o gráfico e a que vai mostrar
        ax1.plot(df['Year'], df['Net Income'], label='lucro', color = 'green', marker='.', markersize = 10, linestyle='-' )
        ax1.plot(x_cordinates, y_cordinates, label='zero', color = 'red', marker='.', markersize = 10, linestyle='--' )

        ax1.set_title(f'Net Profit: {ticker} {company_name}', fontdict={'fontsize': 18}, color= 'black')
        ax1.set_xlabel('Year', color = 'black')
        
        ax1.grid()
        ax1.legend()
        
        
        # Gráfico 2
        
        ax2.plot(df['Year'], df['ND/EBITDA'], label='Dívida', color = 'blue', marker='.', markersize = 10, linestyle='-' )
        ax2.plot(x2_cordinates, y2_cordinates, label='Limite', color = 'red', marker='.', markersize = 10, linestyle='--' )
        
        ax2.grid()
        ax2.legend()
        

if __name__ == '__main__':
    
    ticker = 'Teste'
    company_name = 'Teste'
    df = pd.read_csv('data/balancos_simplificados/A - Agilent Technologies Inc - Simple Balance.csv')
    
    graf_income_debt(df,ticker,company_name)
    