import operator
import time
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import List, Type, Union

import keyboard

from t9keyboard.keyboard_keymap import numpad_character_keys_map, numpad_keyboard_special_keys_map, SpecialAction
from t9keyboard.engine.trie_engine import Trie, SearchPhrase
from t9keyboard.display.display import print_keyboard_layout_helper


@dataclass
class NumpadKey:
    keypad_button: str
    letters: List[str]
    is_special_key: bool = field(default=False)


@dataclass
class SearchResults:
    phrase_counter: int = field(default=0)
    phrase_counter_limit: int = field(default=5)
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

    def set_phrase_counter_limit(self, new_counter_limit: int):
        """
        Setter for phrase_counter_limit.
        :param new_counter_limit: Value which will be set as new phrase_counter_limit
        """
        self.phrase_counter_limit = new_counter_limit


class T9Mode:
    """
    Object for handling all T9Mode actions. It also holds trie object with loaded dictionary.
    trie_engine
    """
    trie_engine: Trie
    last_trie_search: SearchResults
    key_sequence: List[NumpadKey]
    last_pressed_button: Union[NumpadKey, None]

    def __init__(self, custom_dictionary: Path = Path("dictionary/english"), trie: Trie = None):
        # Initialize trie engine - use default one if not given
        self.last_pressed_button = None
        self.trie_engine = trie if trie else Trie()
        # Load dictionary - use default one if not given
        self.load_word_dictionary_from_folder(custom_dictionary)
        # Initialize default lists
        # self.last_trie_search = []
        self.key_sequence = []
        # Get available numpad keyboard keys
        self.available_keys = self.get_available_keyboard_keys()
        # TODO: Find better implementation for storing written text
        self.text_written = "Already written text: "

    def handle_t9_mode(self, mapped_key: NumpadKey):
        # Take input, perform search in t9
        # Show current nums and available letters for each num
        # if there are complete words: display them
        # BONUS: Show words started with current sequence
        # append input to self.key_sequence
        # pass
        # t9_mode.find_words("3"))
        if mapped_key.is_special_key:
            self.perform_special_key_action(mapped_key)
            return
        print_keyboard_layout_helper()
        self.perform_alphabetical_key_action(mapped_key)

        print(self.last_trie_search)

    def find_words(self, numbers: str) -> SearchResults:
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

    # TODO: This method can be unified with single tap mode one
    @staticmethod
    def get_available_keyboard_keys() -> List[NumpadKey]:
        """
        Return list of NumpadKey objects. Need dict with single_tap_keyboard_character_map.
        :return: List of available KeyboardKey objects
        """
        available_keys = []
        for key, values in numpad_character_keys_map.items():
            available_keys.append(NumpadKey(key, values))
        for key, values in numpad_keyboard_special_keys_map.items():
            available_keys.append(NumpadKey(key, values, is_special_key=True))
        return available_keys

    def map_key(self, key: str) -> NumpadKey:
        """
        Map key from input to object of from list of available keyboard buttons.
        NumpadKey object add information about letters values which will be used to perform logic.
        :param key: str Value which represents pressed key
        :return: Matching NumpadKey from available keys
        """
        for index, available_key in enumerate(self.available_keys):
            if key == available_key.keypad_button:
                new_key_object = self.available_keys[index]
                return new_key_object
        raise Exception(f"Could not find {key} in available_keys.")

    def write_character_as_keyboard_input(self, characters: str):
        """
        Write passed character as keyboard input.
        :param characters: String character (or multiple) to write
        :return: None
        """
        time.sleep(0.01)
        keyboard.write(characters)

    def perform_alphabetical_key_action(self, mapped_key: NumpadKey):
        """
        Append written alphabet key to key_sequence.
        Then perform trie search with actual value of key_sequence.
        SearchResults object from trie search will be stored in last_trie_search parameter.
        :param mapped_key: NumpadKey object
        """
        self.key_sequence.append(mapped_key)
        actual_key_sequence = self.get_actual_key_sequence_string()
        self.last_trie_search = self.find_words(actual_key_sequence)

    def perform_special_key_action(self, mapped_key: NumpadKey):
        # WARNING: This requires python >3.10 (case matching method)
        action = getattr(SpecialAction, mapped_key.letters[0])
        match action:
            case SpecialAction.space:
                phrase_to_write = self.last_trie_search.get_current_chosen_phrase().word
                self.write_character_as_keyboard_input(phrase_to_write)
                # TODO: Replace text_written
                self.text_written += " " + phrase_to_write
                print(self.text_written)
                self.store_last_pressed_key()
                # Clear key sequence
                self.key_sequence.clear()
            case SpecialAction.switch_letter:
                if self.last_trie_search:
                    self.last_trie_search.increase_phrase_counter()
                # TODO: Fix gap with missing last trie search.
            case SpecialAction.backspace:
                # TODO: Implement deleting whole word if last action was SpecialAction.space
                # if self.last_pressed_button and self.last_pressed_button.letters==SpecialAction.space
                self.delete_last_character()

    def get_actual_key_sequence_string(self) -> str:
        """
        Loop through self.key_sequence and get digit from every NumpadKey object.
        :return: String with digits from key sequence
        """
        return "".join([num.keypad_button for num in self.key_sequence])

    def store_last_pressed_key(self):
        """
        If key sequence is not clear, save last pressed key to last_pressed_button parameter.
        """
        if self.key_sequence:
            self.last_pressed_button = self.key_sequence[-1]

    def delete_last_character(self):
        """
        Delete last character from input and pop last item from already written key_sequence list
        :return:
        """
        keyboard.send("backspace")
        self.key_sequence.pop()

# TODO: move this as unit tests for T9Mode
# t9_mode = T9Mode()
# t9_mode.load_word_dictionary_from_folder(Path("dictionary/english"))
# print(t9_mode.find_words("3"))  # [[('was', 2), ('war', 1), ('where', 1), ('what', 1)]]
# print(t9_mode.find_words("34"))  # [[('where', 1), ('what', 1)]]
# print(t9_mode.find_words("3482"))  # [[('where', 1), ('what', 1)]]
