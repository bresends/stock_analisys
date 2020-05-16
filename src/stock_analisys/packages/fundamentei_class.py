"""
Classe que lida com os objetos gerados pelo site Fundamentei
Entra autentica e salva páginas a partir de um ticker
"""

import pickle

from bs4 import BeautifulSoup
from selenium import webdriver

import stock_analisys.packages.paths as paths

# =============================================================================
# Class
# =============================================================================

class Fundamentei:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url = f"https://fundamentei.com/us/{ticker}"

    def open_page(self):
        self.driver.get(self.url)

    def autenticate(self):

        self.driver = webdriver.Chrome(paths.bin_path / "chromedriver.exe")

        # Puxa os Cookies
        self.driver.get("https://varvy.com/pagespeed/wicked-fast.html")
        self.driver.implicitly_wait(0.5)

        for cookie in pickle.load(open(paths.bin_path / "cookies_fundamentei.pkl", "rb")):
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)
        print("Cookies Sucessifuly Loaded")

    def html_save(self):
        page_html = self.driver.page_source
        print("Captured")

        with open(
            paths.data_path / "fundamentei" / "full_balances" / f"{self.ticker}.html",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(str(page_html))


def main():
    stock_test = Fundamentei("amzn")
    stock_test.autenticate()
    stock_test.open_page()
    stock_test.html_save()


if __name__ == "__main__":
    main()
