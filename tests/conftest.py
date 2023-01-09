import pytest
from t9keyboard.engine.trie_engine import Trie

"""
Fixtures for tests/test_trie_engine.py
"""
@pytest.fixture
def empty_trie():
    return Trie()


@pytest.fixture
def word_preloaded_trie(empty_trie):
    wha_combo = ["what", "wham", "whats", "whatever"]
    for single_word in wha_combo:
        empty_trie.insert(single_word)
    return empty_trie


@pytest.fixture
def weighted_word_preloaded_trie(empty_trie):
    # Could use T9Mode method for weighting, but it would not be unit testing then
    wha_combo = [("whatever", 4), ("wham", 3), ("whats", 2), ("what", 0)]
    for single_word, weight in wha_combo:
        empty_trie.insert(single_word, weight)
    return empty_trie
