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
#
#
# def my_t9(input_numbers: str) -> List[str]:
#     system_words = get_system_words(DEFAULT_PATH_TO_WORDS_FILE)
#     filtered_system_words_by_len = tuple(filter(
#         lambda word: len(word) == len(input_numbers),
#         system_words))
#     filtered_system_words_by_input = []
#     for word in filtered_system_words_by_len:
#         word_corresponds = True
#         for index, letter in enumerate(word):
#             if letter not in PHONE_KEYS_CONFORMITY[f'{input_numbers[index]}']:
#                 word_corresponds = False
#                 break
#         if word_corresponds:
#             filtered_system_words_by_input.append(word)
#     return filtered_system_words_by_input

#were
#print(my_t9("9373"))

#Step back - implement trie

"""
TrieNode
"""
keypad = {
'2': ['a', 'b', 'c'],
'3': ['d', 'e', 'f'],
'4': ['g', 'h', 'i'],
'5': ['j', 'k', 'l'],
'6': ['m', 'n', 'o'],
'7': ['p', 'q', 'r', 's'],
'8': ['t', 'u', 'v'],
'9': ['w', 'x', 'y', 'z']
}

class TrieNode:
    def __init__(self, weight=0):
        self.children = {}
        self.weight = weight

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, weight):
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.end_of_word = True
        curr.weight = weight

    def search(self, digits):
        words = []
        self.search_recursive(self.root, digits, "", words)
        return words

    def search_recursive(self, node, digits, curr_word, words):
        if not digits:
            if node.end_of_word:
                words.append((curr_word, node.weight))
            return

        digit = digits[0]
        for ch in keypad[digit]:
            if ch in node.children:
                self.search_recursive(node.children[ch], digits[1:], curr_word + ch, words)


#Usage example
trie = Trie()
trie.insert("apple", 1)
trie.insert("app", 2)
trie.insert("banana", 3)
trie.insert("cat", 4)
# print(trie.search("ap"))  # ["apple", "app"]
# print(trie.search("c"))  # ["cat"]
# print(trie.search("ban"))  # ["banana"]
# print(trie.search("z"))  # []
print(trie.search("27753")) # ["apple", "app"]
print(trie.search("228")) # ["cat"]
print(trie.search("222663")) # ["banana"]
print(trie.search("9999")) # []