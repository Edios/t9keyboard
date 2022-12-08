# import pathlib
# from typing import List, Tuple
#
# DEFAULT_PATH_TO_WORDS_FILE = 'words.txt'
# PHONE_KEYS_CONFORMITY = {'2': 'abc',
#                          '3': 'def',
#                          '4': 'ghi',
#                          '5': 'jkl',
#                          '6': 'mno',
#                          '7': 'pqrs',
#                          '8': 'tuv',
#                          '9': 'wxyz'}
#
# def get_system_words(path_to_file: str) -> Tuple:
#     with pathlib.Path(path_to_file).open(mode='r') as stream:
#         file_content = stream.read()
#     words_tuple = tuple(word.strip() for word in file_content.split('\n'))
#     return words_tuple
from typing import List


# Refactored Trie implementation based on: https://albertauyeung.github.io/2020/06/15/python-trie.html/#how-does-a-trie-work
class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char="", word_weight=0):
        self.char = char
        self.word_end = False
        self.word_weight = word_weight
        self.children = {}


class Trie:
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
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

    def dfs(self, node, prefix, store_variable: list):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
            - store_variable: variable which will store search result data
        """
        if node.word_end:
            store_variable.append((prefix + node.char, node.word_weight))

        for child in node.children.values():
            self.dfs(child, prefix + node.char, store_variable)

    def search_for_words_starts_with_prefix(self, prefix: str) -> List[str]:
        """
        Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by word weight.
        :param prefix: Starting chunk of the word
        :return: List of search result
        """

        node = self.root

        for char in prefix:
            if char in node.children:
                node = node.children[char]
                # TODO: Add enumerate to for loop, condition if its a word end and char_counter==len(prefix)
                #  -> append to full word
            else:
                return []

        search_result = []
        self.dfs(node, prefix[:-1], search_result)
        return sorted(list(search_result), key=lambda x: x[1], reverse=True)


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


# Doubled "was" word
trie_words = ["was", "war", "where", "what", "was"]
weighed_words = get_weighed_word_dict(trie_words)

trie_engine = Trie()

for word, weight in weighed_words.items():
    trie_engine.insert(word, weight)
print(trie_engine.search_for_words_starts_with_prefix("wa"))  # [('what', 1), ('where', 1)]


class T9:
    """
    Wishfull:
        Object contains trie with loaded weighed by number of occurances
        As init it takes path to dict

        find_words(numbers):
            input take series of numbers
            product all possible corresponding letters combos of numbers
            use trie.query() with that produced letters combos

            :returns
                [SearchResult]
                    SearchResult
                        Word
                        Weight


    """
