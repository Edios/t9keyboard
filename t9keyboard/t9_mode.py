import operator
import os
import sys
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import List
from t9keyboard.display.gui import Gui, map_digit_to_index_in_map
from t9keyboard.engine.keyboard_writer import KeyboardWriter
from t9keyboard.engine.word_processor import WordProcessor
from t9keyboard.keyboard_keymap import numpad_character_keys_map, numpad_keyboard_special_keys_map, SpecialAction
from t9keyboard.engine.trie_engine import Trie, SearchPhrase


@dataclass
class NumpadKey:
    keypad_button: str
    letters: List[str]
    is_special_key: bool = field(default=False)


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


class T9Mode:
    """
    Object for handling all T9Mode actions. It also holds trie object with loaded dictionary.
    trie_engine
    """
    trie_engine: Trie
    trie_search_results: SearchResults
    writer: KeyboardWriter
    word_processor: WordProcessor
    key_sequence: List[NumpadKey]

    def __init__(self, gui: Gui = None, custom_dictionary: Path = None, trie: Trie = None):
        # Initialize trie engine - use default one if not given
        self.gui = gui if gui else Gui()
        self.trie_engine = trie if trie else Trie()
        self.writer = KeyboardWriter()
        self.word_processor = WordProcessor()
        # Load dictionary - use default one if not given
        if not custom_dictionary: custom_dictionary = list(Path(sys.path[0]).glob("**/dictionary/english"))[0]
        self.load_word_dictionary_from_folder(custom_dictionary)
        # Initialize default lists
        self.trie_search_results = SearchResults()
        self.key_sequence = []
        # Get available numpad keyboard keys
        self.available_keys = self.get_available_keyboard_keys()

    def handle_t9_mode(self, mapped_key: NumpadKey):
        """
        Determine if given mapped_key is special key.
        Base on that perform special or alphabetical key action.
        If trie_search_results is not empty then print
        :param mapped_key: NumpadKey object corresponding with pressed key's
        :return:
        """

        if mapped_key.is_special_key:
            self.perform_special_key_action(mapped_key)
        else:
            self.update_gui_press_digit_button(mapped_key.keypad_button)
            self.perform_alphabetical_key_action(mapped_key)

        self.update_gui_labels()

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
        :param key: int Value which represents pressed key
        :return: Matching NumpadKey from available keys
        """
        for index, available_key in enumerate(self.available_keys):
            if key == available_key.keypad_button:
                new_key_object = self.available_keys[index]
                # WORKAROUND: Mark "7" as special key. It contains punctuation marks and need to be treated in
                # different way.
                if new_key_object.keypad_button == "7": new_key_object.is_special_key = True
                return new_key_object
        raise Exception(f"Could not find {key} in available_keys.")

    def perform_alphabetical_key_action(self, mapped_key: NumpadKey):
        """
        Append written alphabet key to key_sequence.
        Then perform trie search with actual value of key_sequence.
        SearchResults object from trie search will be stored in last_trie_search parameter.
        :param mapped_key: NumpadKey object
        """
        self.key_sequence.append(mapped_key)
        actual_key_sequence = self.get_actual_key_sequence_string()
        self.trie_search_results = self.find_words(actual_key_sequence)

    def perform_special_key_action(self, mapped_key: NumpadKey):
        # WARNING: This requires python >3.10 (case matching method)
        action = getattr(SpecialAction, mapped_key.letters[0], None)
        if not action and mapped_key.keypad_button == "7": action = SpecialAction.seven
        match action:
            case SpecialAction.space:
                """
                When space is pressed, write word as keyboard output.
                Do nothing if trie_search_results is empty.
                """
                self.gui.switch_phrases_highlighted_element(0)
                self.gui.apply_button_highlight(0, is_special_button=True)
                if self.trie_search_results.is_empty():
                    print("Search result is empty, no word to be written")
                    return
                chosen_phrase = self.trie_search_results.get_current_chosen_phrase().word
                self.word_processor.append_characters_to_queue(chosen_phrase)
                self.word_processor.finish_queued_word()
                self.key_sequence.clear()
                self.writer.write(self.word_processor.get_last_word(), add_space=True)

            case SpecialAction.switch_letter:
                """
                Switch actual hint value if search result is not empty.
                """
                self.gui.apply_button_highlight(1, is_special_button=True)
                if not self.trie_search_results.is_empty():
                    self.trie_search_results.increase_phrase_counter()
                    self.gui.switch_phrases_highlighted_element(self.trie_search_results.phrase_counter)
            case SpecialAction.backspace:
                """
                Delete last character by sending backspace.
                If whole word was just typed, delete it by repeating backspace key, remove that word from finished_words 
                """
                self.gui.apply_button_highlight(2, is_special_button=True)
                if not self.word_processor.queued_word and self.word_processor.finished_words and self.key_sequence:
                    self.writer.backspace(
                        repeat_count=self.word_processor.count_last_word_length(count_additional_space=True)
                    )
                    self.word_processor.clear_word_processor_fields()
                    self.trie_search_results.clear_searched_phrases()
                    self.key_sequence.clear()
                else:
                    self.writer.backspace()

                    try:
                        self.key_sequence.pop()
                    except IndexError:
                        print("KeySequence is empty. ")
            case SpecialAction.seven:
                """
                Seven key is responsible for typing punctuation marks. Need to be treated in different way than 
                other digits, that's why this button action is marked as special.
                
                As a simplified version - this key will only use dot.
                """
                self.gui.apply_button_highlight(0, is_special_button=False)
                if self.key_sequence: self.key_sequence.clear()
                self.word_processor.append_characters_to_queue(".")
                self.word_processor.finish_queued_word()
                # self.writer.backspace()
                self.writer.write(self.word_processor.get_last_word(), add_space=True)
            case None:
                print("Special Key action not implemented")

    def get_actual_key_sequence_string(self) -> str:
        """
        Loop through self.key_sequence and get digit from every NumpadKey object.
        :return: String with digits from key sequence
        """
        return "".join([num.keypad_button for num in self.key_sequence])

    def update_gui_labels(self):
        """
        If there are search result in trie_search_results then update gui object.
        Do nothing if search results object .is_empty()
        :return:
        """
        if not self.trie_search_results.is_empty():
            self.gui.update_available_phrases(self.trie_search_results.get_top_phrases())
            self.gui.update_actual_phrase(self.trie_search_results.get_current_chosen_phrase().word)

    def update_gui_press_digit_button(self, keypad_button_digit: str):
        """
        Map digit to list index in gui, then use mapped value to apply button highlighted on gui.
        :param keypad_button_digit:
        :return:
        """
        self.gui.apply_button_highlight(map_digit_to_index_in_map(keypad_button_digit, numpad_character_keys_map))

# TODO: move this as unit tests for T9Mode
# t9_mode = T9Mode()
# t9_mode.load_word_dictionary_from_folder(Path("dictionary/english"))
# print(t9_mode.find_words("3"))  # [[('was', 2), ('war', 1), ('where', 1), ('what', 1)]]
# print(t9_mode.find_words("34"))  # [[('where', 1), ('what', 1)]]
# print(t9_mode.find_words("3482"))  # [[('where', 1), ('what', 1)]]
