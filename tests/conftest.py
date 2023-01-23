from typing import List

import pytest
from t9keyboard.engine.trie_engine import Trie, SearchPhrase

"""
Fixtures for tests/test_trie_engine.py
"""


@pytest.fixture
def empty_trie():
    return Trie()


wha_combo = ["what", "wham", "whats", "whatever"]
wha_combo_weighted = [("whatever", 4), ("wham", 3), ("whats", 2), ("what", 0)]


@pytest.fixture
def word_preloaded_trie(empty_trie):
    for single_word in wha_combo:
        empty_trie.insert(single_word)
    return empty_trie


@pytest.fixture
def weighted_word_preloaded_trie(empty_trie):
    # Could use T9Mode method for weighting, but it would not be unit testing then
    for single_word, weight in wha_combo_weighted:
        empty_trie.insert(single_word, weight)
    return empty_trie


def get_list_of_search_phrases(words: List[tuple]) -> List[SearchPhrase]:
    """
    Get list of SearchPhrases.
    Used for trie_engine testing to avoid repeating same objects.
    :param words: Two element tuple (word,weight)
    :return: List[SearchPhrase]
    """
    result = []
    for elem in words:
        result.append(SearchPhrase(elem[0], elem[1]))
    return result


@pytest.fixture
def words_objects() -> List[SearchPhrase]:
    """
    Get list of weighted SearchPhrases
    Used for trie_engine testing to avoid repeating same objects.
    :return: List[SearchPhrase]
    """
    wha_combo_tuple=[(word,0) for word in wha_combo]
    return get_list_of_search_phrases(wha_combo_tuple)

@pytest.fixture
def words_weighted_objects() -> List[SearchPhrase]:
    """
    Get list of weighted SearchPhrases
    Used for trie_engine testing to avoid repeating same objects.
    :return: List[SearchPhrase]
    """
    return get_list_of_search_phrases(wha_combo_weighted)
