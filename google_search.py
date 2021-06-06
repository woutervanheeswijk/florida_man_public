from typing import List
from googleapiclient.discovery import build
import json
from threading import Thread


def google_search_default(
    search_term: str, api_key: str, cse_id: str, **kwargs
) -> json:
    """Basic Google search request"""
    # Build request
    service = build("customsearch", "v1", developerKey=api_key)

    # Execute request
    query_result = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return query_result


def google_search_thread(
    start: int,
    stop: int,
    num_search_results: int,
    search_term_array: str,
    api_key: str,
    cse_id: str,
    date_list: List[str],
    results_dict: dict,
    **kwargs
) -> None:
    """Google search invoked by thread"""
    for i in range(start, stop):

        # Retrieve search term
        search_term = search_term_array[i]

        # Build request
        service = build("customsearch", "v1", developerKey=api_key)

        # Execute request
        query_result = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()

        for j in range(num_search_results):
            try:
                """Add title to dictionary if containing og:title"""
                title = query_result["items"][j]["pagemap"]["metatags"][0]["og:title"]
                date = date_list[i]
                key = str(date) + "," + str(j)
                results_dict.update({key: title})
            except:
                continue

    return None


def run_query_threads(
    results_dict: dict, search_term_list: List[str], date_list: List[str], my_config
):
    if my_config.num_queries_per_api > 100:
        raise Exception(
            "Custom JSON API does not allow more than 100 requests per day."
        )

    threads = []
    open("query_results.txt", "w")
    for thread_id in range(0, my_config.num_threads):
        start = thread_id * my_config.num_queries_per_api
        stop = min(
            len(search_term_list),
            thread_id * my_config.num_queries_per_api + my_config.num_queries_per_api,
        )

        # Create thread
        t = Thread(
            target=google_search_thread,
            args=(
                start,
                stop,
                my_config.num_results_per_query,
                search_term_list,
                my_config.my_api_keys[thread_id],
                my_config.my_cse_id,
                date_list,
                results_dict,
            ),
            kwargs={"num": my_config.num_results_per_query},
        )
        threads.append(t)

        # Start thread
        t.start()

    # Join such that main thread waits for completion of queries
    for t in threads:
        t.join()

    # Store query results
    with open("query_results.txt", "w") as output_file:
        json.dump(results_dict, output_file)

    return results_dict
