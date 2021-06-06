import re
from typing import Set


def remove_substrings_from_title(
    results_dict: dict, key: str, substring_removal_set: Set[str]
) -> dict:
    """Remove pre-specified substrings from title to match desired style"""
    # Retrieve title from dictionary
    title = results_dict.get(key)

    for substring in substring_removal_set:
        if re.search(substring, title):
            title = title.replace(substring, "")
            results_dict.update({key: title})

    return results_dict


def convert_to_uppercase(string:str) -> str:
    """Capitalize first letter of each word"""
    return string.group(1) + string.group(2).upper()


def remove_end_segments_of_title(results_dict: dict, key: str) -> dict:
    """Remove segments after certain symbols from title (e.g., | media outlet)"""
    # Retrieve title from dictionary
    title = results_dict.get(key)

    # Remove title segments after | or :
    symbol_set = {"|", ":", "("}
    for symbol in symbol_set:
        if symbol in title:
            split_string = title.split(symbol, 1)
            title = split_string[0]
            results_dict.update({key: title})

    return results_dict


def format_title(results_dict: dict, key: str) -> dict:
    """""Format title to uniform style (first letter uppercase, same quotation marks"""

    # Retrieve title from dictionary
    title = results_dict.get(key)

    title = title + " "  # Add white space to end
    title = title.replace(" ‘", ' "')  # Replace quotation marks
    title = title.replace("’ ", '" ')  # Replace quotation marks
    title = title.replace("' ", '" ')  # Replace quotation marks
    title = title.replace(" '", ' "')  # Replace quotation marks
    title = re.sub("(^|\s)(\S)", convert_to_uppercase, title)  # Replace quotation marks
    title = re.sub('(^|")(\S)', convert_to_uppercase, title)  # Replace quotation marks

    results_dict.update({key: title})

    return results_dict
