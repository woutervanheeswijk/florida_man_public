import re
from typing import List


def print_headlines(
    results_dict: dict, date_list: List[str], num_results_per_query: int
) -> None:
    """Print the top headlines per day in the console"""
    for i in range(len(date_list)):
        date = date_list[i]
        for j in range(num_results_per_query):

            key = str(date_list[i]) + "," + str(j)

            try:
                title = results_dict.get(key)
                if title is not None:
                    month = re.sub("[^A-Za-z]+", "", date)
                    str_length = len(month)
                    max_str_len = len("september")
                    num_whitespaces = max_str_len - str_length
                    offset = " " * (num_whitespaces + 1)

                    print(date, offset, title)

                    break
            except:
                continue
    return
