import os
from typing import List, Tuple

import pytest
from pynput.keyboard import KeyCode

from t9keyboard.engine.trie_engine import Trie, SearchPhrase
from t9keyboard.numpad_keyboard import NumpadKeyboard, NumpadKeyboardMode
from t9keyboard.t9_mode import NumpadKey

"""
Fixtures for tests/test_trie_engine.py
"""

words_with_wha = ["what", "wham", "whats", "whatever"]
words_with_wha_weighted = [("whatever", 4), ("wham", 3), ("whats", 2), ("what", 0)]


@pytest.fixture
def empty_trie():
    return Trie()


@pytest.fixture
def word_preloaded_trie(empty_trie):
    for single_word in words_with_wha:
        empty_trie.insert(single_word)
    return empty_trie


@pytest.fixture
def weighted_word_preloaded_trie(empty_trie):
    # Could use T9Mode method for weighting, but it would not be unit testing then
    for single_word, weight in words_with_wha_weighted:
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
    wha_combo_tuple = [(word, 0) for word in words_with_wha]
    return get_list_of_search_phrases(wha_combo_tuple)


@pytest.fixture
def words_weighted_objects() -> List[SearchPhrase]:
    """
    Get list of weighted SearchPhrases
    Used for trie_engine testing to avoid repeating same objects.
    :return: List[SearchPhrase]
    """
    return get_list_of_search_phrases(words_with_wha_weighted)


"""
Fixtures for tests/test_numpad_keyboard.py
"""


#
@pytest.fixture
def five_key() -> Tuple[KeyCode, NumpadKey]:
    """
    Fixture for Numeric Keyboard Key "5" - works only on Windows

    :return: Tuple of
    """
    return KeyCode(vk="101"), NumpadKey("5", ['j', 'k', 'l'], is_special_key=False)


@pytest.fixture
def numpad_keyboard():
    os.chdir("../t9keyboard")
    return NumpadKeyboard()


@pytest.fixture
def numpad_keyboard_t9(numpad_keyboard):
    numpad_keyboard.keyboard_mode = NumpadKeyboardMode.t9
    return numpad_keyboard


@pytest.fixture
def numpad_keyboard_single_tap(numpad_keyboard):
    numpad_keyboard.keyboard_mode = NumpadKeyboardMode.single_tap
    return numpad_keyboard

"""
Fixtures for tests/test_word_processor.py
"""