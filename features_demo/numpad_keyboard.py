import copy
import datetime
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union

import keyboard
from keyboard import KeyboardEvent


class KeypadButton(Enum):
    One = "1"
    Two = "2"
    Three = "3"
    Four = "4"
    Five = "5"
    Six = "6"
    Seven = "7"
    Eight = "8"
    Nine = "9"
    Zero = "0"
    # Special keys
    Star = "*"
    Plus = "+"
    Dot =  "."

    def __repr__(self):
        return str(self.value)

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

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


class SpecialAction:
    pass


@dataclass
class SpecialKey:
    keypad_number: KeypadButton
    action:SpecialAction
    pressed_time: datetime = field(default_factory=datetime.datetime.now)



@dataclass
class AlphabetKey:
    keypad_button: KeypadButton
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


class NumpadKeyboard:
    available_keys: List[AlphabetKey]
    key_sequence: List[AlphabetKey]
    key_pressed_time: datetime

    def __init__(self):
        self.available_keys = self.get_available_alphabet_keys()
        # Default value init
        self.key_sequence = []
    @staticmethod
    def on_press_reaction(event: KeyboardEvent):
        """
        Map keyboard object to KeypadButton enum instance, then execute handle_keypress.
        :param event: KeyboardEvent object from keyboard module
        :return:
        """
        if event.is_keypad == True and KeypadButton.has_value(event.name):
            return keyboard_actions.handle_keypress(KeypadButton(event.name))
    def handle_keypress(self, keypad_button: KeypadButton):
        """
        # TODO: Add proper docstring
        :param keypad_button: Keypad(Enum) Pressed Keypad Key
        :return:
        """
        maped_key = self.map_key(keypad_button)
        if self.is_letter_switch(maped_key):
            self.key_sequence[-1].switch_letter_counter()
            self.write_switched_text_from_key(self.key_sequence[-1].value())
        else:
            self.key_sequence.append(maped_key)
            self.write_character_as_keyboard_input(maped_key.value())
        self.print_text_to_screen()

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
        #Delete previous character
        keyboard.send("backspace")
        time.sleep(0.01)
        self.write_character_as_keyboard_input(character)

    def write_character_as_keyboard_input(self, character: str):
        """
        Take key sequence and write it on focused input (Like normal keyboard).
        # TODO: Change docstring
        # TODO: Already writed text need to be stored in variable? self.written_key_sequence
        :param character: str Character(or multiple) to write
        :return: None
        """
        keyboard.send("backspace")
        time.sleep(0.01)
        keyboard.write(character)

    def is_letter_switch(self, key: AlphabetKey) -> bool:
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

    def map_key(self, key: KeypadButton) -> Union[AlphabetKey]:
        """
        Map key from input to object of from list of available keyboard buttons.
        KeyboardKey object add information about letters values which will be used to perform logic.
        :param key: KeypadButton Enum obj which will be maped to KeyboardKey object
        :return: KeyboardKey corresponding with KeypadButton object
        """
        if key.value.name.isdigit():
            for available_key in self.available_keys:
                if key == available_key.keypad_button:
                    new_key_object = copy.deepcopy(self.available_keys[self.available_keys.index(available_key)])
                    # Default object timestamp need to be refreshed
                    new_key_object.refresh_timestamp()
                    return new_key_object
        else:
            #TODO: Map SpecialKey


    @staticmethod
    def get_available_alphabet_keys() -> List[AlphabetKey]:
        """
        Initialize list with values which can be used.
        :return: List of available KeyboardKey objects
        """
        alphabet_keys = {
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
            'Plus': ['backspace'],
            'Dot' : ['letter_switch']
        }
        available_keys = []
        for key, values in alphabet_keys.items():
            try:
                attribute = getattr(KeypadButton, key)
                available_keys.append(AlphabetKey(attribute, values))
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
    keyboard_actions = NumpadKeyboard()

    keyboard.on_press(keyboard_actions.on_press_reaction)
    while True:
        pass