import time
import webbrowser


import stock_analisys.packages.bastter_class as bc
import stock_analisys.packages.paths as paths
import stock_analisys.packages.plots_bastter as bastter_plot
import stock_analisys.packages.plots_fundamentei as fundamentei_plot


def complete_study(ticker):
    bc.main_extract(ticker)
    webbrowser.open_new_tab(f"https://bastter.com/mercado/stock/{ticker}")
    webbrowser.open_new_tab(
        f"https://financials.morningstar.com/income-statement/is.html?t={ticker}&region=usa&culture=en-US"
    )
    fundamentei_plot.main(ticker)
    bastter_plot.main(ticker)

if __name__ == "__main__":
    complete_study('rost')

