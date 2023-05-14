from dataclasses import dataclass, field
from typing import List
from t9keyboard.display.gui import Gui, map_digit_to_index_in_map
from t9keyboard.engine.keyboard_writer import KeyboardWriter
from t9keyboard.engine.t9_engine import T9Engine, SearchResults
from t9keyboard.engine.word_processor import WordProcessor
from t9keyboard.keyboard_keymap import numpad_character_keys_map, numpad_keyboard_special_keys_map, SpecialAction
from t9keyboard.engine.trie_engine import Trie


@dataclass
class NumpadKey:
    keypad_button: str
    letters: List[str]
    is_special_key: bool = field(default=False)


class T9Mode:
    """
    Object for handling all T9Mode actions. It also holds trie object with loaded dictionary.
    trie_engine
    """
    trie_engine: Trie
    t9_search_results: SearchResults
    writer: KeyboardWriter
    word_processor: WordProcessor
    key_sequence: List[NumpadKey]

    def __init__(self, gui: Gui = None, trie: Trie = None):

        self.gui = gui if gui else Gui()
        self.t9_engine= T9Engine(trie_engine=trie)
        self.writer = KeyboardWriter()
        self.word_processor = WordProcessor()

        # Initialize default lists
        self.t9_search_results = SearchResults()
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
        Append the written alphabet key to key_sequence.
        Then perform trie search with the actual value of key_sequence.
        SearchResults object from trie search will be stored in last_trie_search parameter.
        :param mapped_key: NumpadKey object
        """
        self.key_sequence.append(mapped_key)
        actual_key_sequence = self.get_actual_key_sequence_string()
        self.t9_search_results = self.search_for_word_t9(actual_key_sequence)

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
                if self.t9_search_results.is_empty():
                    print("Search result is empty, no word to be written")
                    return
                chosen_phrase = self.t9_search_results.get_current_chosen_phrase().word
                self.word_processor.append_characters_to_queue(chosen_phrase)
                self.word_processor.finish_queued_word()
                self.key_sequence.clear()
                self.writer.write(self.word_processor.get_last_word(), add_space=True)

            case SpecialAction.switch_letter:
                """
                Switch actual hint value if search result is not empty.
                """
                self.gui.apply_button_highlight(1, is_special_button=True)
                if not self.t9_search_results.is_empty():
                    self.t9_search_results.increase_phrase_counter()
                    self.gui.switch_phrases_highlighted_element(self.t9_search_results.phrase_counter)
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
                    self.t9_search_results.clear_searched_phrases()
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
                #self.writer.backspace()
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
        if not self.t9_search_results.is_empty():
            self.gui.update_available_phrases(self.t9_search_results.get_top_phrases())
            self.gui.update_actual_phrase(self.t9_search_results.get_current_chosen_phrase().word)

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
