import copy
import datetime
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Union

import keyboard
from keyboard import KeyboardEvent

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
numpad_keyboard_character_map = {
    '7': ['.', ',', '?', '!'],
    '8': ['a', 'b', 'c'],
    '9': ['d', 'e', 'f'],
    '4': ['g', 'h', 'i'],
    '5': ['j', 'k', 'l'],
    '6': ['m', 'n', 'o'],
    '1': ['p', 'q', 'r', 's'],
    '2': ['t', 'u', 'v'],
    '3': ['w', 'x', 'y', 'z'],
    '0': [' ', '0', '\n'],
    '+': ['backspace'],
    '-': ['switch_keyboard_mode'],
    '.': ['switch_letter'],
    'enter': ['enter']
}


class NumpadKeyboardMode(Enum):
    single_press = auto()
    t9 = auto()


class SpecialAction(Enum):
    backspace = "backspace"
    switch_keyboard_mode = "switch_keyboard_mode"


@dataclass
class NumpadKey:
    keypad_button: str
    letters: List[str]
    is_special_key: bool = field(default=False)
    letter_counter: int = field(default=0)
    switched_letter_value: bool = field(default=False)
    pressed_time: datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.is_special_key = True if len(self.letters) < 2 else False

    def value(self) -> str:
        """
        Get actual chosen letter
        :return: str Value of current letter corresponding with letter_counter
        """
        return self.letters[self.letter_counter]

    def switch_letter_counter(self):
        """
        Switch letter counter for getting another value of letter and switch
        :return: None
        """
        if self.letter_counter < len(self.letters) - 1:
            self.letter_counter += 1
        else:
            self.letter_counter = 0

        self.switched_letter_value = True

    def refresh_timestamp(self):
        self.pressed_time = datetime.datetime.now()


class NumpadKeyboard:
    keyboard_mode: NumpadKeyboardMode
    available_keys: List[NumpadKey]
    key_sequence: List[NumpadKey]
    key_pressed_time: datetime

    def __init__(self):
        self.available_keys = self.get_available_keyboard_keys()
        # Default value init
        self.key_sequence = []
        self.keyboard_mode = NumpadKeyboardMode.single_press

    def on_press_reaction(self, keypad_button: KeyboardEvent):
        """
        # TODO: Add proper docstring
        :param keypad_button: Keypad(Enum) Pressed Keypad Key
        :return:
        """
        if not keypad_button.is_keypad == True:
            return
        mapped_key = self.map_key(keypad_button.name)
        if self.keyboard_mode == NumpadKeyboardMode.single_press:
            self.handle_single_press_mode(mapped_key)
        if self.keyboard_mode==NumpadKeyboardMode.t9:
            # TODO: Mapped key have too much information for t9. Refactor to base class
            self.handle_t9_mode(mapped_key)

    def print_text_to_screen(self):
        """
        Writes actual self.key_sequence to the screen
        :return: None
        """
        if self.key_sequence:
            print_value = ""
            for letter in self.key_sequence:
                print_value += letter.value()
            print(print_value)

    def write_switched_text_from_key(self, character: str):
        """
        Send backspace button for deleting last character, then use write method to replace that with switched character
        This method need to handle letter switch as deleting last character and replacing with new one.
        :param character:
        :return: None
        """
        # WA: Delete previous character by sending backspace
        self.delete_last_character()
        time.sleep(0.01)
        self.write_character_as_keyboard_input(character)

    def write_character_as_keyboard_input(self, character: str):
        """
        Take key sequence and write it on focused input (Like normal keyboard).
        # TODO: Change docstring
        :param character: str Character(or multiple) to write
        :return: None
        """
        self.delete_last_character()
        time.sleep(0.01)
        keyboard.write(character)

    def is_letter_switch(self, key: NumpadKey) -> bool:
        """
        If detection time is less than 2 second and last keypad_button value is same as self.key_sequence[-1]
        :param key:
        :return: Bool if letter should be switch
        """
        # TODO: Inversion will make it more readable?
        if self.key_sequence and \
                self.timedelta_in_seconds_between_two_dates(self.key_sequence[-1].pressed_time, key.pressed_time, 2) and \
                key.keypad_button == self.key_sequence[-1].keypad_button:
            return True
        return False

    def map_key(self, key: str) -> Union[NumpadKey]:
        """
        Map key from input to object of from list of available keyboard buttons.
        KeyboardKey object add information about letters values which will be used to perform logic.

        :param key: str Value which represents pressed key
        :return: KeyboardKey corresponding with KeypadButton object
        """
        for available_key in self.available_keys:
            if key == available_key.keypad_button:
                new_key_object = copy.deepcopy(self.available_keys[self.available_keys.index(available_key)])
                # Default object timestamp need to be refreshed
                new_key_object.refresh_timestamp()
                return new_key_object

    @staticmethod
    def get_available_keyboard_keys() -> List[NumpadKey]:
        """
        Return list of NumpadKey objects. Need dict with numpad_keyboard_character_map.
        :return: List of available KeyboardKey objects
        """
        available_keys = []
        for key, values in numpad_keyboard_character_map.items():
            available_keys.append(NumpadKey(key, values))
        return available_keys

    @staticmethod
    def timedelta_in_seconds_between_two_dates(start: datetime.datetime, stop: datetime, delta: int) -> bool:
        """
        Is difference between start and stop less than delta.
        This method supports delta input as seconds
        :param start: datetime date
        :param stop: datetime date
        :param delta: int delta which would be added
        :return: Return True if time difference between start and stop is less than delta
        """
        elapsed_time = stop - start
        return True if elapsed_time <= datetime.timedelta(seconds=delta) else False

    def handle_single_press_mode(self, mapped_key):
        if mapped_key.is_special_key:
            # TODO: Handle special action
            self.perform_special_key_action(mapped_key)
        elif self.is_letter_switch(mapped_key):
            self.key_sequence[-1].switch_letter_counter()
            self.write_switched_text_from_key(self.key_sequence[-1].value())
        else:
            self.key_sequence.append(mapped_key)
            self.write_character_as_keyboard_input(mapped_key.value())

        self.print_text_to_screen()

    def handle_t9_mode(self, mapped_key):
        #Take input, perform search in t9
        # Show current nums and available letters for each num
        # if there are complete words: display them
        # BONUS: Show words started with current sequence
        # append input to self.key_sequence
        pass

    def perform_special_key_action(self, mapped_key):
        # WARNING: This requires python >3.10 (case matching method)
        action = getattr(SpecialAction, mapped_key.value())
        match action:
            case SpecialAction.backspace:
                # Need to delete plus character, then actual character
                self.delete_last_character()
                self.delete_last_character()
            case SpecialAction.switch_keyboard_mode:
                self.switch_keyboard_mode()

    def delete_last_character(self):
        """
        Delete last character from input.
        #[..]and pop last item from already written key_sequence list
        :return:
        """
        keyboard.send("backspace")
        # self.key_sequence.pop()

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
