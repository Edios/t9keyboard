from itertools import product
from typing import List

from t9keyboard.numpad_keyboard import numpad_keyboard_character_map


# Refactored Trie implementation based on: https://albertauyeung.github.io/2020/06/15/python-trie.html/#how-does-a-trie-work
class TrieNode:
    """
    Single node of Trie structure
    """

    def __init__(self, char="", word_weight=0):
        self.char = char
        self.word_end = False
        self.word_weight = word_weight
        self.children = {}


class Trie:
    """
    Main Trie object.
    """

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character.
        """
        self.root = TrieNode()

    def insert(self, word, weight=0):
        """
        Insert word into trie.
        Weight can be added to word, which will be used to sort result of search method.
        :param word:
        :param weight:
        :return:
        """
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.word_end = True

        # Increment the counter to indicate that we see this word once more
        node.word_weight = weight

    def dfs(self, node, prefix, store_variable: list, full_words_only=False):
        """
        Depth-first traversal of the trie
        :param node: the node to start with
        :param prefix: the current prefix, for tracing a word while traversing the trie
        :param store_variable: variable which will store traversal data
        :param full_words_only: return only list of full words

        :return None (dfs result will be stored in store_variable list)
        """
        if node.word_end:
            store_variable.append((prefix + node.char, node.word_weight))
        if not full_words_only:
            for child in node.children.values():
                self.dfs(child, prefix + node.char, store_variable)

    def search_for_words_starts_with_prefix(self, prefix: str, full_words_only: bool = False) -> List[str]:
        """
        Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by word weight but prioritize full word.

        :param prefix: Starting chunk of the word
        :param full_words_only: Return only list of full words
        :return: List of search result
        """

        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        full_words = []
        self.dfs(node, prefix[:-1], full_words, True)

        search_result = []
        self.dfs(node, prefix[:-1], search_result, full_words_only)

        return self.sort_results(full_words, search_result)

    @staticmethod
    def sort_results(priority_words: List, search_result: List) -> List:
        """
        Nest two list search results into one, where priority words will be on the beginning of the list.

        :param priority_words: Words what need to be on beginning of the list
        :param search_result: Rest of the search result which would be sorted by word weight
        :return: List of nested search results with prioritized full words
        """

        if priority_words==search_result: return priority_words
        # Remove word which exists in dfs search results
        for word in priority_words:
            if word in search_result: search_result.remove(word)
        priority_words.append(sorted(search_result, key=lambda x: x[1], reverse=True))
        return priority_words


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


# TODO: move this as unit tests for Trie

## Doubled "was" word
trie_words = ["was", "war", "where", "what", "was", "wa", "whey", "whe"]
# weighed word dict moved to T9 class
weighed_words = T9.get_weighed_word_dict(trie_words)

trie_engine = Trie()

for word, weight in weighed_words.items():
    trie_engine.insert(word, weight)
print(trie_engine.search_for_words_starts_with_prefix("whe",
                                                      full_words_only=False))  # [('whe', 1), ('where', 1), ('whey', 1)]
print(trie_engine.search_for_words_starts_with_prefix("whe", full_words_only=True))  # [('whe', 1)]

# TODO: move this as unit tests for T9
# t9_engine = T9()
# print(t9_engine.find_words("3"))  # [[('was', 2), ('war', 1), ('where', 1), ('what', 1)]]
# print(t9_engine.find_words("34"))  # [[('where', 1), ('what', 1)]]
# print(t9_engine.find_words("3482"))  # [[('where', 1), ('what', 1)]]
