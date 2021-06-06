def create_taboo_set() -> set:
    """Create set of title taboos to be removed from dictionary"""
    taboo_set = {
        "Headlines",
        "Viral",
        "Challenge",
        "#",
        "?",
        "Top",
        "Twitter",
        "Facebook",
        "Kill",
        "Murder",
        "Death",
        "Gallery",
        "Photos",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "Year",
        "2020",
        "r/",
        "Zodiac",
        "Story",
        "Stories",
        "News",
    }

    # Add lowercase and uppercase variants of each word
    taboo_set_lower = set()
    taboo_set_upper = set()

    for taboo in taboo_set:
        taboo_lower = taboo.lower()
        taboo_upper = taboo.upper()
        taboo_set_lower.add(taboo_lower)
        taboo_set_upper.add(taboo_upper)

    taboo_set.update(taboo_set_lower)
    taboo_set.update(taboo_set_upper)

    return taboo_set


def create_substring_removal_set() -> set:
    """Create set of substrings to be removed from titles"""
    substring_removal_set = {
        " - NBC2 News ",
        " - Rolling Out ",
        " - Vanyaland ",
        ", Deputies Say",
        ", Police Say",
        ", Officials Say",
        ", Cops Say",
        ' " Police Say',
        ' " Deputies Say',
    }

    return substring_removal_set


def create_key_removal_set() -> set:
    """Create set of keys to be removed from dictionary"""
    key_removal_set = set()

    return key_removal_set
