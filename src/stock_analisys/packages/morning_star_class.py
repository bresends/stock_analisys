"""
Morning Star Companies Info Extract  
"""

import pandas as pd
from selenium import webdriver

import stock_analisys.packages.paths as paths


class MorningStar:
    """
    Super Class for all related tasks for MorningStar
    """

    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url = f"https://financials.morningstar.com/ratios/r.html?t={ticker}"

    def open_browser(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : str(paths.morning_star / 'key_ratios')}
        chrome_options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path=str(paths.bin_path / "chromedriver.exe"),
        )


class MorningStarExtract(MorningStar):

    """
    Methods related to download the csv files from MorningStar
    """

    def open_page(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)

    def key_ratios_export(self):

        export_buttom = self.driver.find_element_by_link_text("Export")

        # Se está carregado, passa pra frente, senão para.
        if export_buttom.is_displayed():

            export_buttom.click()
        else:

            print("Button not found in page")

    def scroll_page_to_botton(self):
        self.driver.implicitly_wait(2)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")


def main(ticker):
    stock_obj = MorningStarExtract(ticker)
    stock_obj.open_browser()
    stock_obj.open_page()
    stock_obj.key_ratios_export()
    stock_obj.scroll_page_to_botton()


if __name__ == "__main__":
    
    df = pd.read_csv(paths.morning_star/ 'tickers.csv')
    for item in df['Ticker']:
        main(item.strip())
