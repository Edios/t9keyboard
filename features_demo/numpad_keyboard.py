import copy
import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import List

import keyboard


class KeypadKey(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Zero = 0

    def __repr__(self):
        return str(self.value)


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


@dataclass
class KeyboardKey:
    keypad_number: KeypadKey
    letters: List[str]
    letter_counter: int = field(default=0)
    switched_letter_value: bool = field(default=False)
    pressed_time: datetime = field(default_factory=datetime.datetime.now)

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


class KeyboardActions:
    available_keys: List[KeyboardKey]
    key_sequence: List[KeyboardKey]
    key_pressed_time: datetime

    def __init__(self):
        self.available_keys = self.get_available_keys()
        # Default value init
        self.key_sequence = []

    def handle_keypress(self, keypad_button: KeypadKey):
        """
        # TODO: Add proper docstring
        :param keypad_button: Keypad(Enum) Pressed Keypad Key
        :return:
        """
        maped_key = self.map_key(keypad_button)
        if self.is_letter_switch(maped_key):
            self.key_sequence[-1].switch_letter_counter()
        else:
            self.key_sequence.append(maped_key)
        self.write_text()

    def write_text(self):
        """
        Writes actual self.key_sequence to the screen as letters
        :return: None
        """
        if self.key_sequence:
            print_value = ""
            for letter in self.key_sequence:
                print_value += letter.value()
            print(print_value)

    def write_switched_text_from_key(self, character: str):
        """
        Write \b for deleting last character, then use write method to replace that with switched character
        This method need to handle letter switch as deleting last character and replacing with new one.
        :param character:
        :return: None
        """
        #Delete previous character
        keyboard.send("backspace")
        self.write_character_as_keyboard_input(character)

    def write_character_as_keyboard_input(self, character: str):
        """
        Take key sequence and write it on focused input (Like normal keyboard).
        # TODO: Change docstring
        # TODO: Already writed text need to be stored in variable? self.written_key_sequence
        :param character: str Character(or multiple) to write
        :return: None
        """
        keyboard.write(character)

    def is_letter_switch(self, key: KeyboardKey) -> bool:
        """
        If detection time is less than 2 second and last keypad_button value is same as self.key_sequence[-1]
        :param key:
        :return: Bool if letter should be switch
        """
        # TODO: Inversion will make it more readable?
        if self.key_sequence and \
                self.timedelta_in_seconds_between_two_dates(self.key_sequence[-1].pressed_time, key.pressed_time, 2) and \
                key.keypad_number == self.key_sequence[-1].keypad_number:
            return True
        return False

    def map_key(self, key: KeypadKey) -> KeyboardKey:
        """
        Map key from input to object of from list of available keyboard buttons.
        KeyboardKey object add information about letters values which will be used to perform logic.
        :param key: KeypadKey Enum obj which will be maped to KeyboardKey object
        :return: KeyboardKey corresponding with KeypadKey object
        """
        for available_key in self.available_keys:
            if key == available_key.keypad_number:
                new_key_object = copy.deepcopy(self.available_keys[self.available_keys.index(available_key)])
                # Default object timestamp need to be refreshed
                new_key_object.refresh_timestamp()
                return new_key_object

    @staticmethod
    def get_available_keys() -> List[KeyboardKey]:
        """
        Initialize list with values which can be used.
        :return: List of available KeyboardKey objects
        """
        t9_values = {
            'Seven': ['.', ',', '?', '!'],
            'Eight': ['a', 'b', 'c'],
            'Nine': ['d', 'e', 'f'],
            'Four': ['g', 'h', 'i'],
            'Five': ['j', 'k', 'l'],
            'Six': ['m', 'n', 'o'],
            'One': ['p', 'q', 'r', 's'],
            'Two': ['t', 'u', 'v'],
            'Three': ['w', 'x', 'y', 'z'],
            'Zero': [' ', '0', '\n'],
        }
        available_keys = []
        for key, values in t9_values.items():
            try:
                attribute = getattr(KeypadKey, key)
                available_keys.append(KeyboardKey(attribute, values))
            except AttributeError:
                # TODO: Replace print with logger
                print("Could not match Keypad Key with t9 value")
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


if __name__ == '__main__':
    keyboard_actions = KeyboardActions()
    # keyboard_actions.available_keys[2].switch_letter_counter()
    # keyboard_actions.available_keys[2].switch_letter_counter()
    # keyboard_actions.available_keys[2].switch_letter_counter()
    # keyboard_actions.available_keys[2].switch_letter_counter()
    # keyboard_actions.available_keys[2].value()

    keyboard.add_hotkey('num 9', keyboard_actions.handle_keypress, args=[KeypadKey.Nine])
    keyboard.add_hotkey('num 8', keyboard_actions.handle_keypress, args=[KeypadKey.Eight])
    keyboard.add_hotkey('num 7', keyboard_actions.handle_keypress, args=[KeypadKey.Seven])
    keyboard.add_hotkey('num 6', keyboard_actions.handle_keypress, args=[KeypadKey.Six])
    keyboard.add_hotkey('num 5', keyboard_actions.handle_keypress, args=[KeypadKey.Five])
    keyboard.add_hotkey('num 4', keyboard_actions.handle_keypress, args=[KeypadKey.Four])
    keyboard.add_hotkey('num 3', keyboard_actions.handle_keypress, args=[KeypadKey.Three])
    keyboard.add_hotkey('num 2', keyboard_actions.handle_keypress, args=[KeypadKey.Two])
    keyboard.add_hotkey('num 1', keyboard_actions.handle_keypress, args=[KeypadKey.One])
    keyboard.add_hotkey('num 0', keyboard_actions.handle_keypress, args=[KeypadKey.Zero])
