"""
Plot generating Module

"""
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
#     Graph Plot
# =============================================================================


def income_graph(df, ticker, company_name):

    # Size and Style
    plt.style.use('default')
    plt.figure(figsize=(10, 10))


    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    ticker = 'Teste'
    company_name = 'Teste'
    df = pd.read_csv(
        'data/simplified_balances/A - Agilent Technologies Inc - Simple Balance.csv')

    income_graph(df, ticker, company_name)















# Fourth Plot 

ax[1][1].plot(ages, dev_salaries, color='#444444',
         linestyle='--', label='All Devs')

ax[1].plot(ages, py_salaries, label='Python')
ax2.plot(ages, js_salaries, label='JavaScript')

ax1[.legend()
ax1.set_title('Median Salary (USD) by Age')
ax1.set_ylabel('Median Salary (USD)')

ax2.legend()
ax2.set_xlabel('Ages')
ax2.set_ylabel('Median Salary (USD)')













    fig, ax = plt.subplots(nrows=1, ncols=3)

    """
    First Plot = Net Income graph

    """
    # Plots Net Income line
    ax[0][0].plot(df['Year'], df['Net Income'],
                  color='green',
                  linestyle='-',
                  marker='.',
                  markersize=10,
                  label='lucro')

    # Plots Zero line for Net Income
    x_cordinates = [df['Year'].iloc[0],
                    df['Year'].iloc[-1]
                    ]
    y_cordinates = [0, 0]

    ax[0][0].plot(x_cordinates, y_cordinates,
                  color='red',
                  linestyle='--',
                  marker='.',
                  markersize=10,
                  label='zero')

    # Plot Config
    ax[0][0].set_title(f'Net Profit: {ticker} - {company_name}',
                       fontdict={'fontsize': 18},
                       color='black')

    ax[0][0].set_xlabel('Year', color='black')
    ax[0][0].set_ylabel('Net Profit (mil)', color='black')
    ax[0][0].legend()










plt.legend()
    plt.grid()
    plt.tick_params(colors='black')
    plt.xticks(df['Year'])



    ax[0][0].bar(ages, dev_salaries,
                color='red',
                linestyle='--',
                label='All Devs')

    ax[0][0].set_title('Median Salary (USD) by Age')
    ax[0][0].set_ylabel('Ages')
    ax[0][0].set_xlabel('Median Salary (USD)')



    # Second Plot 
    ax[0][1].plot(ages, dev_salaries,
                color='green',
                linestyle='-',
                label='All Devs')

    ax[0][1].set_title('Median Salary (USD) by Age')
    ax[0][1].set_ylabel('Ages')
    ax[0][1].set_xlabel('Median Salary (USD)')
    ax[0][1].legend()

    # Third Plot 
    ax[1][0].plot(ages, dev_salaries, color='#444444',
            linestyle='--', label='All Devs')

    plt.tight_layout()
    plt.show()