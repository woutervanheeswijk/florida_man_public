from typing import List, Set
from difflib import SequenceMatcher
import re


def compute_sentence_overlap(headline_1: str, headline_2: str) -> float:
    """Compute overlap between sentences using SequenceMatcher"""
    s = SequenceMatcher(lambda x: x == " ", headline_1, headline_2)

    return s.ratio()


def remove_similar_titles(
    date_index: int,
    time_delta: int,
    overlap_threshold: int,
    num_search_results: int,
    list_of_dates: List[str],
    results_dict: dict,
    key: str,
) -> dict:
    """
    Remove top headlines having high overlap with reference headline, looking
    time_delta days ahead of the reference date. Only top headlines need to be
    removed in case of a match.
    """
    # Remove Florida Man from title
    title_1 = results_dict.get(key)
    title_1_adj = title_1.replace("Florida Man", "")
    title_1_adj.lower()
    re.sub(r"[^\w]", " ", title_1_adj)

    for i in range(date_index + 1, date_index + time_delta):
        date = list_of_dates[i]
        for j in range(num_search_results):

            key = str(date) + "," + str(j)
            try:
                title_2 = results_dict.get(key)

                # Remove Florida Man from title
                title_2_adj = title_2.replace("Florida Man", "")
                title_2_adj.lower()
                re.sub(r"[^\w]", " ", title_2_adj)

                # Compute overlap between titles
                overlap_ratio = compute_sentence_overlap(title_1_adj, title_2_adj)

                # Remove if overlap exceeds specified threshold
                if overlap_ratio > overlap_threshold:
                    results_dict.pop(key)
            except:
                continue
    return results_dict


def remove_overlapping_sentences(
    results_dict: dict, date_list: List[str], my_config
) -> dict:
    """Remove all titles overlapping with preceding titles from dictionary"""
    for i in range(len(date_list)):
        for j in range(my_config.num_results_per_query):

            # Generate key
            key = str(date_list[i]) + "," + str(j)
            try:
                # Retrieve title from dictionary
                title = results_dict.get(key)

                if title is not None:
                    results_dict = remove_similar_titles(
                        i,
                        my_config.time_delta,
                        my_config.overlap_threshold,
                        my_config.num_results_per_query,
                        date_list,
                        results_dict,
                        key,
                    )
            except:
                continue

    return results_dict


def remove_title_taboo(results_dict: dict, key: str, taboo_set: Set[str]) -> dict:
    """Remove titles containing taboo words from dictionary"""
    # Retrieve title from dictionary
    title = results_dict.get(key)

    for taboo in taboo_set:
        if taboo in title:
            results_dict.pop(key)
            break
    return results_dict


def remove_specified_keys_from_dictionary(
    results_dict: dict, key_removal_set: Set[str]
) -> dict:
    """Remove elements with manually specified keys from dictionary"""
    for key in key_removal_set:
        results_dict.pop(key)

    return results_dict


def check_florida_man(results_dict: dict, key: str) -> dict:
    """Remove all titles that do not start with 'Florida Man'"""
    # Retrieve title from dictionary
    title = results_dict.get(key)

    # Check if title starts with 'Florida Man'
    if re.search("^Florida Man", title) is None:
        results_dict.pop(key)

    return results_dict
