import copy
import time
#import tkinter as tk
#from tkinter import ttk
from dataclasses import dataclass, field
from enum import Enum
from typing import Union, List

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

    def value(self) -> str:
        """
        Get actual chosen letter
        :return: str Value of current letter corresponding with letter_counter
        """
        return self.letters[self.letter_counter]

    def switch_letter_counter(self):
        """
        Switch letter counter for getting another value of letter.
        :return: None
        """
        if self.letter_counter < len(self.letters) - 1:
            self.letter_counter += 1
        else:
            self.letter_counter = 0


class KeyboardActions:
    available_keys: List[KeyboardKey]
    key_sequence: List[KeyboardKey]
    key_pressed_time: float

    def __init__(self):
        self.available_keys = self.get_available_keys()
        # Default value init
        self.key_pressed_time = time.time()
        self.key_sequence = []

    def handle_keypress(self, keypad_button: KeypadKey):
        """
        Add value to self.key_sequence list
        Uses:
            self.key_sequence
            self.last_key_time

        If detection time is less than 2 second = consider it as switch_letter
        If detection time is over 2 second = consider it as add_letter
        :param keypad_button: Keypad(Enum) Pressed Keypad Key
        :return:
        """
        maped_key = self.map_key(keypad_button)
        # TODO: Add setter for key_pressed_time
        self.key_pressed_time = time.time()

        # TODO: Fix bug with multiple keypresses - is letter switch do not work correctly
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

    def is_letter_switch(self, key: KeyboardKey) -> bool:
        """
        If detection time is less than 2 second and last keypad_button value is same as self.key_sequence[-1]
        :param key:
        :return: Bool if letter should be switcself.key_sequence = {list: 2} [KeyboardKey(keypad_number=5, letters=['j', 'k', 'l'], letter_counter=1), KeyboardKey(keypad_number=5, letters=['j', 'k', 'l'], letter_counter=1)]hed or not
        """
        actual_time = time.time()
        # TODO: Inversion will make it more readable?
        if self.key_sequence and actual_time - self.key_pressed_time < 2 and \
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
                return copy.deepcopy(self.available_keys[self.available_keys.index(available_key)])

    def get_available_keys(self) -> List[KeyboardKey]:
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


import keyboard

# def handle_key(key):
#     print(key)


keyboard_actions = KeyboardActions()
keyboard_actions.available_keys[2].switch_letter_counter()
keyboard_actions.available_keys[2].switch_letter_counter()
keyboard_actions.available_keys[2].switch_letter_counter()
keyboard_actions.available_keys[2].switch_letter_counter()
keyboard_actions.available_keys[2].value()

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
