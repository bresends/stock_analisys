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
        # label="lucro",
    )

    # Zero mark
    a[0].axhline(
        color="red", linestyle="--", marker=".", markersize=10,  # label="zero",
    )

    # Plot Config
    a[0].fill_between(
        df["Year"],
        df["Net Income"],
        where=(df["Net Income"] > 0),
        color="g",
        alpha=0.75,
        interpolate=True,
        label="Profit",
    )

    # Plot Config
    a[0].fill_between(
        df["Year"],
        df["Net Income"],
        where=(df["Net Income"] < 0),
        color="r",
        alpha=0.75,
        interpolate=True,
        label="Loss",
    )

    a[0].set_title(
        f"Net Income {ticker} - {company_name}",
        fontdict={"fontsize": 12},
        color="black",
    )

    a[0].set_xlabel("Year", color="black")
    a[0].set_ylabel("Net Profit (mil)", color="black")
    a[0].grid()
    a[0].legend()

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
        # label="Debt",
    )

    # Control line for debt
    a[1].axhline(
        y=3, color="red", linestyle="--", marker=".", markersize=10,  # label="zero",
    )

    # Plot Config
    a[1].fill_between(
        df["Year"],
        df["ND/EBITDA"],
        y2=3,
        where=(df["ND/EBITDA"] < 3),
        color="b",
        alpha=0.75,
        interpolate=True,
        label="Debt Free",
    )

    a[1].fill_between(
        df["Year"],
        df["ND/EBITDA"],
        y2=3,
        where=(df["ND/EBITDA"] > 3),
        color="r",
        alpha=0.8,
        interpolate=True,
        label="Debt",
    )

    a[1].set_title(
        f"Debt/EBITDA: {ticker} - {company_name}",
        fontdict={"fontsize": 12},
        color="black",
    )

    a[1].set_xlabel("Year", color="black")
    a[1].set_ylabel("Net Profit (mil)", color="black")
    a[1].grid()
    a[1].legend()

    """
    Variation in Income
    """

    var_pos = df[df["%"] >= 0]
    var_neg = df[df["%"] < 0]

    a[2].bar(
        var_pos["Year"], var_pos["%"], color="green", label="Profit",
    )

    a[2].bar(
        var_neg["Year"], var_neg["%"], color="red", label="Drop",
    )

    # Zero mark
    a[2].axhline(
        color="red", linestyle="--", marker=".", markersize=10, #label="zero",
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
    a[2].legend()

    # Effective Plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    ticker = "Whatever"
    company_name = "The company"
    df = pd.read_csv(
        "data/simplified_balances/CAT - Caterpillar Inc - Simple Balance.csv"
    )

    data_graph(df, ticker, company_name)
