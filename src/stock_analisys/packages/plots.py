"""
Plot generating Module

"""
import pandas as pd
import matplotlib.pyplot as plt

def data_graph(df, ticker, company_name):

    """
    Graph ploting function
    """

    plt.style.use("default")
    fig, a = plt.subplots(1, 3, figsize=(14, 5))

    """
    Income
    """
    # Plots Net Income line
    a[0].plot(
        df["Year"],
        df["Net Income"],
        color="green",
        linestyle="-",
        marker=".",
        markersize=10,
        label="lucro",
    )

    # Plots Zero line for Net Income
    x_cordinates = [df["Year"].iloc[0], df["Year"].iloc[-1]]
    y_cordinates = [0, 0]

    a[0].plot(
        x_cordinates,
        y_cordinates,
        color="red",
        linestyle="--",
        marker=".",
        markersize=10,
        label="zero",
    )

    # Plot Config
    a[0].set_title(
        f"Net Income {ticker} - {company_name}",
        fontdict={"fontsize": 12},
        color="black",
    )
    a[0].set_xlabel("Year", color="black")
    a[0].set_ylabel("Net Profit (mil)", color="black")
    a[0].grid()

    """
    Debt Plot Axis
    """
    a[1].plot(
        df["Year"],
        df["ND/EBITDA"],
        color="blue",
        linestyle="-",
        marker=".",
        markersize=10,
        label="lucro",
    )

    # Plots Zero line for Net Income
    x_cordinates = [df["Year"].iloc[0], df["Year"].iloc[-1]]
    y_cordinates = [3, 3]

    a[1].plot(
        x_cordinates,
        y_cordinates,
        color="red",
        linestyle="--",
        marker=".",
        markersize=10,
        label="zero",
    )

    # Plot Config
    a[1].set_title(
        f"Debt/EBITDA: {ticker} - {company_name}",
        fontdict={"fontsize": 12},
        color="black",
    )

    a[1].set_xlabel("Year", color="black")
    a[1].set_ylabel("Net Profit (mil)", color="black")
    a[1].grid()

    """
    Variation in Income
    """
    a[2].bar(
        df["Year"], df["%"], color="green", label="lucro",
    )

    # Plots Zero line for Net Income
    x_cordinates = [df["Year"].iloc[0], df["Year"].iloc[-1]]
    y_cordinates = [0, 0]

    a[2].plot(
        x_cordinates,
        y_cordinates,
        color="red",
        linestyle="--",
        marker=".",
        markersize=10,
        label="zero",
    )

    # Plot Config
    a[2].set_title(
        f"Net Income %: {ticker} - {company_name}",
        fontdict={"fontsize": 12},
        color="black",
    )

    a[2].set_xlabel("Year", color="black")
    a[2].set_ylabel("Net Profit (mil)", color="black")
    a[2].grid()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    ticker = "AAA"
    company_name = "The company"
    df = pd.read_csv(
        "data/simplified_balances/A - Agilent Technologies Inc - Simple Balance.csv"
    )

    data_graph(df, ticker, company_name)
