import operator
from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchPhrase:
    word: str
    weight: int
    exact_search_word: bool = field(default=False)

    def __post_init__(self):
        """
        Add +1 word weight if dfs search marked it as exact_search_word
        """
        if self.exact_search_word:
            self.weight += 1

    def __repr__(self):
        return self.word


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

    Refactored Trie implementation based on tutorial from:
        https://albertauyeung.github.io/2020/06/15/python-trie.html/#how-does-a-trie-work
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
        :param word: Desired word to be added into Trie structure
        :param weight: Weight of the word used to sort it in trie
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
        node.word_weight = weight

    def dfs(self, node: TrieNode, prefix: str, store_variable: list, full_words_only=False):
        """
        Depth-first traversal of the trie
        :param node: the node to start with
        :param prefix: the current prefix, for tracing a word while traversing the trie
        :param store_variable: variable which will store traversal data
        :param full_words_only: return only list of full words

        :return Dfs result will be stored in store_variable. It will contain SearchPhrase objects.
        """
        if node.word_end:
            store_variable.append(
                SearchPhrase(prefix + node.char, node.word_weight, True if full_words_only else False))
        if not full_words_only:
            for child in node.children.values():
                self.dfs(child, prefix + node.char, store_variable)

    def search_for_words_starts_with_prefix(self, prefix: str, full_words_only: bool = False) -> List[SearchPhrase]:
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
        # Get list of full words to prioritize them in sort method
        self.dfs(node, prefix[:-1], full_words, True)

        search_result = []
        self.dfs(node, prefix[:-1], search_result, full_words_only)

        return self.sort_results(full_words, search_result)

    @staticmethod
    def sort_results(priority_words: List[SearchPhrase], search_result: List[SearchPhrase]) -> List[SearchPhrase]:
        """
        Nest two list search results into one, where priority words will be on the beginning of the list.

        :param priority_words: Words what need to be on beginning of the list
        :param search_result: Rest of the search result which would be sorted by word weight
        :return: List of nested search results with prioritized full words
        """

        if priority_words == search_result: return priority_words
        # Remove word which exists in dfs search results
        search_result_words = [elem.word for elem in search_result]
        for search_phrase in priority_words:
            if search_phrase.word in search_result_words:
                search_result.pop(search_result_words.index(search_phrase.word))
        search_result = sorted(search_result, key=operator.attrgetter('weight'), reverse=True)
        priority_words.extend(search_result)
        return priority_words
