"""
Plot generating Module

"""
import matplotlib.pyplot as plt
import pandas as pd
import operator

import stock_analisys.packages.bastter_class as bc


class BastterPlots:

    """
        Makes the Bastter Plots 
    """

    def __init__(self, tables):
        self.tables = tables

    def bs_plot(
        self,
        field,
        table_number=0,
        line_color="b",
        fill_between=False,
        fill_threshold=0,
        invert_fill=False,
    ):

        """
            Plots HTML field tables from Bastter
        """
        df = self.tables[table_number]

        "Setting Fig"
        fig = plt.figure()
        fig.set_size_inches(10, 6)
        plot = fig.add_subplot(111)

        plot.plot(
            df["Year"],
            df[field],
            color=line_color,
            linestyle="-",
            marker=".",
            markersize=8,
        )

        # Zero mark
        plot.axhline(
            y=fill_threshold, color="red", linestyle="--", marker=".", markersize=10
        )

        def fill():

            """
                Fill function
            """

            # Inverts the colors for the debt
            if not invert_fill:
                where_fill_1 = df[field] > fill_threshold
                where_fill_2 = df[field] < fill_threshold
            else:
                where_fill_1 = df[field] < fill_threshold
                where_fill_2 = df[field] > fill_threshold

            # Fill Positive
            plot.fill_between(
                df["Year"],
                df[field],
                y2=fill_threshold,
                where=(where_fill_1),
                color=line_color,
                alpha=0.75,
                interpolate=True,
                label=f"+{field}",
            )

            # Fill Negative

            plot.fill_between(
                df["Year"],
                df[field],
                y2=fill_threshold,
                where=(where_fill_2),
                color="r",
                alpha=0.95,
                interpolate=True,
                label=f"-{field}",
            )

        fill()

        plot.set_title(
            field, fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel(field, color="black")
        plot.grid()
        plot.legend()

        plt.tight_layout()
        plt.show()

    def bs_bar(
        self, field, table_number=0, bar_collor="b", bar_threshold=0,
    ):

        """
            Plots Bars for the HTML field tables from Bastter
        """
        df = self.tables[table_number]

        """
            Variation in Income
        """

        var_pos = df[df[field] >= 0]
        var_neg = df[df[field] < 0]

        "Setting Fig"
        fig = plt.figure()
        fig.set_size_inches(9, 5)
        plot = fig.add_subplot(111)

        plot.bar(var_pos["Year"], var_pos[field], color=bar_collor, label=f"+{field}")

        plot.bar(var_neg["Year"], var_neg[field], color="red", label=f"-{field}")

        # Zero mark
        plot.axhline(
            y=bar_threshold, color="red", linestyle="--", marker=".", markersize=10
        )

        plot.set_title(
            field, fontsize=12, color="black",
        )

        plot.set_xlabel("Year", color="black")
        plot.set_ylabel(field, color="black")
        plot.grid()
        plot.legend()

        plt.show()


def main(ticker):

    stock_obj = bc.BastterEvaluate(ticker)
    pandas_tables = stock_obj.tables_extract()
    plots = BastterPlots(pandas_tables)

    plots.bs_plot(
        field="Net Income",
        table_number=0,
        line_color="g",
        fill_between=True,
        fill_threshold=0,
    )

    try:
        plots.bs_bar(
            field="%-Net Income", table_number=0, bar_collor="g", bar_threshold=0,
        )
    except:
        print("Not possible to print Variance")

    plots.bs_plot(
        field="Earnings per Share",
        table_number=0,
        line_color="indigo",
        fill_between=True,
        fill_threshold=0,
    )

    try:
        plots.bs_bar(
            field="%-Earnings per Share",
            table_number=0,
            bar_collor="indigo",
            bar_threshold=0,
        )
    except:
        print("Not possible to print Variance")

    plots.bs_plot(
        field="Net Debt / EBITDA",
        table_number=0,
        line_color="b",
        fill_between=True,
        fill_threshold=2,
        invert_fill=True,
    )

    plots.bs_plot(
        field="EBITDA",
        table_number=0,
        line_color="gold",
        fill_between=True,
        fill_threshold=0,
    )

    plots.bs_plot(
        field="EBIT",
        table_number=0,
        line_color="orange",
        fill_between=True,
        fill_threshold=0,
    )

    plots.bs_plot(
        field="Net Profit Margin",
        table_number=0,
        line_color="crimson",
        fill_between=True,
        fill_threshold=20,
    )

    plots.bs_plot(
        field="Debt", table_number=0, line_color="red", fill_between=False,
    )

    plots.bs_plot(
        field="Net Debt", table_number=0, line_color="firebrick", fill_between=False,
    )

    plots.bs_plot(
        field="Net Debt/Equity",
        table_number=0,
        line_color="darkcyan",
        fill_between=True,
        fill_threshold=1,
        invert_fill=True,
    )

    plots.bs_plot(
        field="Equity",
        table_number=0,
        line_color="rebeccapurple",
        fill_between=True,
        fill_threshold=0,
    )

    plots.bs_plot(
        field="Cash",
        table_number=0,
        line_color="dodgerblue",
        fill_between=True,
        fill_threshold=0,
    )


if __name__ == "__main__":
    main("msft")
