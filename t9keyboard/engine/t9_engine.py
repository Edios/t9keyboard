from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import List

from t9keyboard.keyboard_keymap import numpad_character_keys_map
from t9keyboard.engine.trie_engine import Trie


@dataclass
class NumpadKey:
    keypad_button: str
    letters: List[str]
    is_special_key: bool = field(default=False)


class T9:
    """
    Object for handling all T9 actions. It also holds trie object with loaded dictionary.
    trie_engine
    """
    trie_engine: Trie

    def __init__(self, trie=None):
        self.trie_engine = trie if trie else Trie()

    def find_words(self, numbers: str) -> List:
        """
        Take series of numbers, produces all possible letters combos of them and search for word in Trie.
        :param numbers: Input numbers with range from 1 to 9.
        :return: List of possible words to be constructed from input numbers
        """
        combo_list = self._product_combos(numbers)
        found_words = []
        for single_phrase in combo_list:
            found_phases = self.trie_engine.search_for_words_starts_with_prefix(single_phrase)
            if found_phases:
                found_words.extend(found_phases)
        return found_words

    def load_word_dictionary_from_folder(self, directory_path: Path):
        """
        Take all .txt files in directory and add them to Trie tree.
        :param directory_path: Words file, separated by newline
        :return:
        """
        list_of_words = []
        for path in self._get_files_from_directory_which_matches_pattern(directory_path, "*.txt"):
            list_of_words.extend(self._read_words_from_file(path))

        weighted_words = self._get_weighed_word_dictionary(list_of_words)
        self.load_weighted_words_into_trie_dictionary(weighted_words)

    @staticmethod
    def _get_weighed_word_dictionary(word_list: List[str]) -> dict:
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
    def _product_combos(self, numbers: str, character_map: dict = numpad_character_keys_map) -> List[str]:
        """
        Produce all possible combinations of letters from a given set of numbers.
        :param numbers: List of input numbers
        :param character_map: Character mapping dictionary.
        :return: List of all combined letters
        """
        characters_to_combo = [character_map[number] for number in numbers]
        return [''.join(produced_tuple) for produced_tuple in product(*characters_to_combo)]

    @staticmethod
    def _read_words_from_file(file_path: Path) -> List:
        # TODO: Could nest this check into one method
        if not file_path.is_file():
            raise FileNotFoundError(f"File path do not exists: {file_path}")
        return file_path.read_text().split("\n")

    @staticmethod
    def _get_files_from_directory_which_matches_pattern(directory: Path, pattern: str) -> List[Path]:
        """
        Glob on directory to search for pattern.
        :param directory: Path object, need to be folder
        :param pattern: pattern to glob method
        :return: list of  matching files
        """
        # TODO: Could nest this check into one method
        if not directory.is_dir():
            raise FileNotFoundError(f"File path do not exists: {directory}")
        return list(directory.glob(pattern))

    def load_weighted_words_into_trie_dictionary(self, weighted_words: dict):
        """
        Add every dictionary item to Trie tree.
        :param weighted_words: Dictionary which each node contains key=node and value=word word_weight
        :return:
        """
        for word, weight in weighted_words.items():
            self.trie_engine.insert(word, weight)

    def map_key(self, key: str):
        pass

# TODO: move this as unit tests for T9
# t9_engine = T9()
# t9_engine.load_word_dictionary_from_folder(Path("dictionary/english"))
# print(t9_engine.find_words("3"))  # [[('was', 2), ('war', 1), ('where', 1), ('what', 1)]]
# print(t9_engine.find_words("34"))  # [[('where', 1), ('what', 1)]]
# print(t9_engine.find_words("3482"))  # [[('where', 1), ('what', 1)]]
