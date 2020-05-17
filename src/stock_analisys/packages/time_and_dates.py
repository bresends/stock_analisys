"""
Module related to dealing with times and dates conversions
"""

import time


def print_lines():
    print("----------------------------------------------------")


def print_txt_inside_lines(str_txt):
    print(f"########## {str_txt} ###########")


def time_it_secs_conversion(start_time: float, end_time: float):
    """Deal with the conversion of seconds to minutes of hour when dealing with timming

    Arguments:
        start_time {float} -- [The Beggining of Execution]
        end_time {float} -- [The end Of Exectuion]
    """
    elapsed_time = end_time - start_time

    if elapsed_time < 60:
        print_lines()
        print(f"Time in execution = {elapsed_time:.2f} seconds")
        print_txt_inside_lines("Done")

    elif elapsed_time > 3600:
        time_hours = elapsed_time / 3600
        print(f"Time in execution = {time_hours:.2f} Hours")
        print_txt_inside_lines("Done")
    else:
        time_minutes = elapsed_time / 60
        print_lines()
        print(f"Tempo gasto na execução = {time_minutes:.2f} minutos")
        print_txt_inside_lines("Done")


def main():
    time_it_secs_conversion(0, 200)


if __name__ == "__main__":
    main()
