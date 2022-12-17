from itertools import product
from typing import List

from t9keyboard.numpad_keyboard import numpad_keyboard_character_map
from t9keyboard.trie_engine import Trie


class T9:
    trie_engine: Trie
    """
    T9 object
    """

    def __init__(self, trie=None, word_dictionary=None):
        self.trie_engine = trie if trie else Trie()
        self.load_trie_word_dictionary(word_dictionary)

    def find_words(self, numbers: str) -> List:
        """
        Take series of numbers, produces all possible letters combos of them and search for word in Trie.
        :param numbers: Input numbers with range from 1 to 9.
        :return: List of possible words to be constructed from input numbers
        """
        combo_list = self._product_combos(numbers)
        found_words = []
        for single_phrase in combo_list:
            found_phares = self.trie_engine.search_for_words_starts_with_prefix(single_phrase)
            if found_phares:
                found_words.append(found_phares)
        return found_words

    def load_trie_word_dictionary(self, word_dictionary=None, weighted_words=False):
        # TODO: Use bool for weighted words
        # TODO: ITS testing code with no dictionary. Use dictionary for this
        if not word_dictionary:
            trie_words = ["was", "war", "where", "what", "was"]
            weighed_words = self.get_weighed_word_dict(trie_words)
            for word, weight in weighed_words.items():
                self.trie_engine.insert(word, weight)

    @staticmethod
    def get_weighed_word_dict(word_list: List[str]) -> dict:
        """
        Count each element in list. Increase word_weight parameter (value of dict) if word is multiplied in list.
        :param word_list: List of words to be weighed
        :return: Dictionary which each node contains key=node and value=word word_weight
        """
        weighted_words = {}
        for word in word_list:
            weighted_words[word] = weighted_words.get(word, 0) + 1
        return weighted_words

    # TODO: Separate character_map dict with it default value
    def _product_combos(self, numbers: str = "456", character_map: dict = numpad_keyboard_character_map) -> List[str]:
        """
        Produce all possible combinations of letters from a given set of numbers.
        :param numbers: List of input numbers
        :param character_map: Character mapping dictionary.
        :return: List of all combined letters
        """
        characters_to_combo = [character_map[number] for number in numbers]
        return [''.join(produced_tuple) for produced_tuple in product(*characters_to_combo)]

# TODO: move this as unit tests for T9
# t9_engine = T9()
# print(t9_engine.find_words("3"))  # [[('was', 2), ('war', 1), ('where', 1), ('what', 1)]]
# print(t9_engine.find_words("34"))  # [[('where', 1), ('what', 1)]]
# print(t9_engine.find_words("3482"))  # [[('where', 1), ('what', 1)]]
