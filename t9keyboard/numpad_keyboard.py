from enum import Enum, auto
from pathlib import Path

import keyboard
from keyboard import KeyboardEvent

from t9keyboard.engine.t9_engine import T9
from t9keyboard.single_tap_keyboard_mode import SingleTapKey, SingleTapMode
from t9keyboard.t9_mode import T9Mode

# TODO: Print this graphics as helper
"""
    +-------+-------+-------+
    |   7   |   8   |   9   |
    |  .?!  |  ABC  |  DEF  |
    +-------+-------+-------+
    |   4   |   5   |   6   |
    |  GHI  |  JKL  |  MNO  |
    +-------+-------+-------+
    |   1   |   2   |   3   |
    | PQRS  |  TUV  |  WXYZ |
    +-------+-------+-------+
    |   *   |   0   |   #   |
    |   ←   | SPACE |   →   |
    +-------+-------+-------+
"""


class NumpadKeyboardMode(Enum):
    single_press = auto()
    t9 = auto()


class SpecialAction(Enum):
    backspace = "backspace"
    switch_keyboard_mode = "switch_keyboard_mode"


class NumpadKeyboard:
    keyboard_mode: NumpadKeyboardMode
    t9_engine: T9

    single_tap_mode: SingleTapMode
    t9_mode: T9Mode

    def __init__(self):
        #Default keyboard mode
        self.keyboard_mode = NumpadKeyboardMode.t9

        #TODO: move t9 engine to t9_mode.py
        self.t9_engine = T9()
        self.t9_engine.load_word_dictionary_from_folder(Path("dictionary/english"))
        self.last_trie_search = []

    def on_press_reaction(self, keypad_button: KeyboardEvent):
        """
        This method should be triggered by keyboard.on_press which produces KeyboardEvent.
        :param keypad_button: KeyboardEvent Pressed Keypad Key
        :return:
        """
        if not keypad_button.is_keypad == True:
            return
        # TODO: Map key should map key for mode

        if self.keyboard_mode == NumpadKeyboardMode.single_press:
            mapped_key = self.single_tap_mode.map_single_tap_key(keypad_button.name)
            self.single_tap_mode.handle_single_press_mode(mapped_key)
        if self.keyboard_mode == NumpadKeyboardMode.t9:
            # TODO: Mapped key have too much information for t9. Refactor to base class
            #self.handle_t9_mode(mapped_key)
            pass

    def handle_t9_mode(self, mapped_key: SingleTapKey):
        # Take input, perform search in t9
        # Show current nums and available letters for each num
        # if there are complete words: display them
        # BONUS: Show words started with current sequence
        # append input to self.key_sequence
        # pass
        # t9_engine.find_words("3"))

        # TODO: Remove single_tap_mode dependencies - Own key mapping for T9 mode
        if mapped_key.keypad_button == "0":
            # TODO: There's a bug with nesting list on search - reproduce sequence 5642
            self.single_tap_mode.write_character_as_keyboard_input(self.last_trie_search[0][0][0])
        self.single_tap_mode.key_sequence.append(mapped_key)
        # TODO: its WA
        self.last_trie_search = self.t9_engine.find_words("".join([num.keypad_button for num in self.single_tap_mode.key_sequence]))

        print(self.last_trie_search)

    def switch_keyboard_mode(self):
        # TODO: Match current keyboard mode in enum, then switch it
        # self.keyboard_mode=
        pass


if __name__ == '__main__':
    # TODO: Consider checking platform. Keyboard suppress is working only on windows. Workaround for Linux is to send
    #  backspaces
    keyboard_actions = NumpadKeyboard()

    keyboard.on_press(keyboard_actions.on_press_reaction)
    while True:
        pass
