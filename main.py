# -*- coding: utf-8 -*-
"""
Created on Fri May 28 20:55:35 2021
This Python script searches a Google Custom Search Engine, running four parallel Google CSE JSON API threads.
The queries return the top ten results for each day of the year, pertaining to the 'Florida Man' meme.
The og:titles are retrieved from the results and formatted in a common style.
Titles are removed based on a taboo search and an overlap check.
The remaining top title per day is printed in the console.
A masked word cloud is generated, containing the most common words.

For external use, please fill in your personal API keys and CSE ID in config.py, and set refresh_query_results to 'True'
The free version of the Google CSE JSON API allows a maximum of 100 request per day.

@author: Wouter van Heeswijk
GNU General Public License v3.0
6 June 2021
"""

# Import libraries
import json
from datetime import date

# Import functions from other modules
from taboo_list import (
    create_taboo_set,
    create_substring_removal_set,
    create_key_removal_set,
)
from generate_word_cloud import generate_word_cloud
from text_formatting import (
    format_title,
    remove_end_segments_of_title,
    remove_substrings_from_title,
)
from text_operations import (
    remove_overlapping_sentences,
    remove_title_taboo,
    remove_specified_keys_from_dictionary,
    check_florida_man,
)
from time_operations import create_list_of_days
from google_search import run_query_threads
from print_console import print_headlines
from config import create_configuration


if __name__ == "__main__":
    """Search and process headlines containing the 'Florida Man' theme, using the Google Custom Search Engine via the Google CSE JSON API."""
    # Initialize results dictionary
    results_dict = dict()

    # Generate list of days (day-month format)
    date_list = list(create_list_of_days(date(2020, 1, 1), date(2020, 12, 31)))

    # Create list of search queries
    search_term_list = ["Florida Man " + date for date in date_list]

    # Initialize configuration
    my_config = create_configuration(search_term_list)

    #  from google_search import google_search_default
    if my_config.refresh_query_results:
        # Find results from Google Custom Search Engine (requires active Google Custom Search API)
        results_dict = run_query_threads(
            results_dict, search_term_list, date_list, my_config
        )
    else:
        # Load query results
        with open("query_results.txt", "r") as json_file:
            results_dict = json.load(json_file)

    # Create taboo sets
    taboo_set = create_taboo_set()
    key_removal_set = create_key_removal_set()
    substring_removal_set = create_substring_removal_set()

    # Remove all titles not meeting criteria
    for i in range(len(date_list)):
        date = date_list[i]
        for j in range(my_config.num_results_per_query):

            # Generate dictionary key
            key = str(date_list[i]) + "," + str(j)

            try:

                # Format title to desired style
                results_dict = format_title(results_dict, key)
                results_dict = remove_end_segments_of_title(results_dict, key)
                results_dict = remove_substrings_from_title(
                    results_dict, key, substring_removal_set
                )

                # Check whether title starts with 'Florida Man'
                results_dict = check_florida_man(results_dict, key)

                # Remove titles containing taboo words from dictionary
                results_dict = remove_title_taboo(results_dict, key, taboo_set)

                # Remove titles containing pre-defined keys from dictionary
                results_dict = remove_specified_keys_from_dictionary(
                    results_dict, key_removal_set
                )
            except:
                continue

    # For remaining headlines, remove overlapping headlines

    results_dict = remove_overlapping_sentences(results_dict, date_list, my_config)

    # Print top headlines in console
    print_headlines(results_dict, date_list, my_config.num_results_per_query)

    # Generate word cloud
    generate_word_cloud(results_dict, date_list, my_config.num_results_per_query)
