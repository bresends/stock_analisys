"""
Morning Star Companies Info Extract  
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time 

import stock_analisys.packages.paths as paths


class MorningStar:
    """
    Super Class for all related tasks for MorningStar
    """

    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url_income = f"http://financials.morningstar.com/income-statement/is.html?t={ticker}"
        self.url_keys = f"http://financials.morningstar.com/ratios/r.html?t={ticker}"

    def set_browser_to_financials(self):
        self.url = self.url_income
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : str(paths.morning_star_path / 'income_statement')}
        chrome_options.add_experimental_option('prefs', prefs)

        self.driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path=str(paths.bin_path / "chromedriver.exe"),
        )
    
    def set_browser_to_key_ratios(self):
        self.url = self.url_keys
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : str(paths.morning_star_path / 'key_ratios')}
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

        # If button is loaded, continues
        if export_buttom.is_displayed():

            export_buttom.click()

            time.sleep(2)
        else:

            print("Button not found in page")

    def scroll_page_to_botton(self):
        self.driver.implicitly_wait(2)
        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    
    def income_statement_export(self):
        
        action = ActionChains(self.driver)

        export_buttom = self.driver.find_element_by_xpath('//*[@id="sfcontent"]/div[1]/div[2]/div[21]/span/a')

        # Se está carregado, passa pra frente, senão para.
        if export_buttom.is_displayed():
            action.move_to_element(export_buttom).perform()
            export_buttom.click()
            time.sleep(1)
        else:

            print("Button not found in page")


def key_ratios_extract(ticker):
    stock_obj = MorningStarExtract(ticker)
    stock_obj.set_browser_to_key_ratios()
    stock_obj.open_page()
    stock_obj.key_ratios_export()
    stock_obj.scroll_page_to_botton()

def income_extract(ticker):
    stock_obj = MorningStarExtract(ticker)
    stock_obj.set_browser_to_financials()
    stock_obj.open_page()
    stock_obj.income_statement_export()
    stock_obj.scroll_page_to_botton()

def main(ticker):
    key_ratios_extract(ticker)
    income_extract(ticker)


if __name__ == "__main__":
    main('rost')