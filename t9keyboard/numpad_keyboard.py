from enum import Enum, auto
from pathlib import Path

import keyboard
from keyboard import KeyboardEvent

from t9keyboard.engine.t9_engine import T9, NumpadKey
from t9keyboard.single_tap_keyboard_mode import SingleTapKey, SingleTapMode
from t9keyboard.t9_mode import T9Mode


# TODO: Print this graphics as helper
def print_keyboard_layout_helper():
    print(
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
    )


class NumpadKeyboardMode(Enum):
    single_press = auto()
    t9 = auto()


class NumpadKeyboard:
    keyboard_mode: NumpadKeyboardMode
    t9_engine: T9

    single_tap_mode: SingleTapMode
    t9_mode: T9Mode

    def __init__(self):
        # Default keyboard mode
        self.keyboard_mode = NumpadKeyboardMode.t9
        # TODO: move t9 engine to t9_mode.py
        self.t9_engine = T9()
        self.t9_engine.load_word_dictionary_from_folder(Path("dictionary/english"))
        self.last_trie_search = []

        # load single tap mode
        self.single_tap_mode = SingleTapMode()

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
            mapped_key = self.single_tap_mode.map_key(keypad_button.name)
            self.single_tap_mode.handle_single_press_mode(mapped_key)
        if self.keyboard_mode == NumpadKeyboardMode.t9:
            # TODO: Mapped key have too much information for t9. Refactor to base class
            # mapped_key=self.t9_engine.map_key(keypad_button.name)
            mapped_key = self.t9_engine.map_key(keypad_button.name)
            self.handle_t9_mode(mapped_key)
            pass

    def handle_t9_mode(self, mapped_key: NumpadKey):
        # Take input, perform search in t9
        # Show current nums and available letters for each num
        # if there are complete words: display them
        # BONUS: Show words started with current sequence
        # append input to self.key_sequence
        # pass
        # t9_engine.find_words("3"))

        if mapped_key.keypad_button == "0":
            self.single_tap_mode.write_character_as_keyboard_input(self.last_trie_search[0].word)
            return
        print_keyboard_layout_helper()
        self.t9_engine.key_sequence.append(mapped_key)
        # TODO: its WA
        self.last_trie_search = self.t9_engine.find_words(
            "".join([num.keypad_button for num in self.single_tap_mode.key_sequence]))

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
