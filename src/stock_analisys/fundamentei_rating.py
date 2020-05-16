from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

# =============================================================================
# Directories Setup
# =============================================================================

cwd_path = Path.cwd()
data_path = cwd_path / "data"
fundamentei_balances = data_path / "fundamentei" / "full_balances"
bin_path = cwd_path / "bin"  


if __name__ == "__main__":



    print(table.prettify())
