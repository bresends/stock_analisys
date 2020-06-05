"""
Module related to dealing with times and dates conversions
"""

import time
import functools


def print_line():
    print("----------------------------------------------------")


def print_txt_inside_lines(str_txt):
    print(f"########## {str_txt} ###########")


def time_it(func):

    @functools.wraps(func)
    def time_it_wrapper(*args, **kwargs):

        start_time = time.time()

        func_return = func(*args, **kwargs)

        end_time = time.time()

        elapsed_time = end_time - start_time

        if elapsed_time < 60:
            print_line()
            print(f"Function: {func.__name__!r} executed in {elapsed_time:.2f} seconds")
            print_txt_inside_lines("Done")

        elif elapsed_time > 3600:
            time_hours = elapsed_time / 3600
            print(f"Function: {func.__name__!r} executed in {time_hours:.2f} hours")
            print_txt_inside_lines("Done")
        else:
            time_minutes = elapsed_time / 60
            print_line()
            print(f"Function: {func.__name__!r} executed {time_minutes:.2f} minutes")
            print_txt_inside_lines("Done")
        
        return func_return

    return time_it_wrapper

@time_it
def test(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])

if __name__ == "__main__":
    test(10)
