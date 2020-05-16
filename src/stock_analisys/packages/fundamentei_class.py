from pathlib import Path
from selenium import webdriver
import pickle
from bs4 import BeautifulSoup

# =============================================================================
# Directories Setup
# =============================================================================

cwd_path = Path.cwd()
data_path = cwd_path / "data"
bin_path = cwd_path / "bin"


class Fundamentei:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.url = f"https://fundamentei.com/us/{ticker}"

    def open_page(self):
        self.driver.get(self.url)

    def autenticate(self):

        self.driver = webdriver.Chrome(bin_path / "chromedriver.exe")

        # Puxa os Cookies
        self.driver.get("https://varvy.com/pagespeed/wicked-fast.html")
        self.driver.implicitly_wait(0.5)

        for cookie in pickle.load(open(bin_path / "cookies_fundamentei.pkl", "rb")):
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)
        print("Cookies Sucessifuly Loaded")

    def html_save(self):
        page_html = self.driver.page_source
        print("Captured")

        with open(
            data_path / "fundamentei" / "full_balances" / f"{self.ticker}.html",
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
