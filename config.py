from dataclasses import dataclass, field
from math import ceil
from typing import List


def create_configuration(search_term_list: List[str]):
    """Create configuration"""
    # Computable search engine key
    MY_CSE_ID = "CSE_ID"

    # Google API keys
    MY_API_KEYS = [
        "API_KEY1",
        "API_KEY2",
        "API_KEY3",
        "API_KEY4",
    ]

    TIME_DELTA = 10                             # Time horizon for removing overlapping titles
    OVERLAP_THRESHOLD = 0.6                     # Minimal overlap ratio for removing overlapping titles
    NUM_THREADS = 4                             # Number of search threads running
    NUM_QUERIES_PER_API = ceil(
        len(search_term_list) / NUM_THREADS
    )                                           # Number of queries per API
    NUM_RESULTS_PER_QUERY = 10                  # Number of search results per query

    def get_api_keys() -> List[str]:
        """Function to read API keys"""
        return MY_API_KEYS

    @dataclass(frozen=True)
    class Config:
        refresh_query_results: bool = field(default=False)
        my_cse_id: str = field(default=MY_CSE_ID)
        my_api_keys: List[str] = field(default_factory=get_api_keys)
        time_delta: int = field(default=TIME_DELTA)
        overlap_threshold: float = field(default=OVERLAP_THRESHOLD)
        num_threads: int = field(default=NUM_THREADS)
        num_queries_per_api: int = field(default=NUM_QUERIES_PER_API)
        num_results_per_query: int = field(default=NUM_RESULTS_PER_QUERY)

    my_config = Config()

    return my_config
