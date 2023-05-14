import operator
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from t9keyboard.engine.trie_engine import Trie, SearchPhrase


@dataclass
class SearchResults:
    phrase_counter: int = field(default=0)
    phrase_counter_limit: int = field(default=4)
    search_phrases: List = field(default_factory=lambda: [])

    def get_current_chosen_phrase(self) -> SearchPhrase:
        """
        Get search phrase from search_phrases list.
        It will return 'n' element from list where 'n' is phrase_counter
        :return: SearchPhrase
        """
        return self.get_phrase_from_search_results(self.phrase_counter)

    def get_phrase_from_search_results(self, position_in_list: int) -> SearchPhrase:
        """
        Get search phrase from search_phrases list.
        :param position_in_list: Position of item in search_phrases
        :return:
        """
        return self.search_phrases[position_in_list]

    def increase_phrase_counter(self):
        if self.phrase_counter < self.phrase_counter_limit:
            self.phrase_counter += 1
        else:
            self.phrase_counter = 0

    def sort(self):
        """
        Sort search_phrases by theirs weight
        :return:
        """
        self.search_phrases = sorted(self.search_phrases, key=operator.attrgetter('weight'), reverse=True)

    def validate_phrase_counter_limit(self):
        """
        Check if phrase counter limit do not exceed list of search phrases length.
        If possitive, set length as new phrase counter limit
        """
        if self.phrase_counter_limit > self.search_phrases.__len__():
            self.phrase_counter_limit = self.search_phrases.__len__()

    def get_top_phrases(self) -> List[str]:
        """
        Get slice of search_phrases list with stop value of phrase_counter_limit.
        :return:
        """
        return self.search_phrases[slice(0, self.phrase_counter_limit + 1)]

    def is_empty(self) -> bool:
        """
        Check if Search results is empty.
        :return: Return True if its search_phrases is empty.
        """
        return True if not self.search_phrases else False

    def clear_searched_phrases(self):
        """
        Clear search_phrases and counter.
        :return:
        """
        self.search_phrases = []
        self.phrase_counter = 0


class T9Engine:
    def __init__(self, trie_engine: Trie = None, dictionary_folder: Path = Path("dictionary/english")):
        self.trie_engine = trie_engine if trie_engine else Trie()
        self.load_word_dictionary_from_folder(dictionary_folder)

    def search_for_word_t9(self, numbers: str) -> SearchResults:
        """
        Take series of numbers, produces all possible letters combos of them and search for word in Trie.
        :param numbers: Input numbers with range from 1 to 9.
        :return: List of possible words to be constructed from input numbers
        """
        combo_list = self._product_combos(numbers)
        search_results = SearchResults()
        for single_phrase in combo_list:
            found_phases = self.trie_engine.search_for_words_starts_with_prefix(single_phrase)
            if found_phases:
                search_results.search_phrases.extend(found_phases)
            # Word list need to be sorted again
        search_results.sort()
        # If length of phrases is below default phrase_counter_limit, change it to len of phrases list
        search_results.validate_phrase_counter_limit()
        return search_results

    def search_for_word_t9(self, numbers: str) -> SearchResults:
        """
        Take series of numbers, produces all possible letters combos of them and search for word in Trie.
        :param numbers: Input numbers with range from 1 to 9.
        :return: List of possible words to be constructed from input numbers
        """
        combo_list = self._product_combos(numbers)
        search_results = SearchResults()
        for single_phrase in combo_list:
            found_phases = self.trie_engine.search_for_words_starts_with_prefix(single_phrase)
            if found_phases:
                search_results.search_phrases.extend(found_phases)
            # Word list need to be sorted again
        search_results.sort()
        # If length of phrases is below default phrase_counter_limit, change it to len of phrases list
        search_results.validate_phrase_counter_limit()
        return search_results

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
