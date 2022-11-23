"""
# from pynput.keyboard import Key, Listener
#
# def on_press(key):
#     print('{0} pressed'.format(
#         key))
#
# def on_release(key):
#     print('{0} release'.format(
#         4862139784key))
#     if key == Key.esc:
#         # Stop listener
#
#         return False
#
# # Collect events until released
# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

#######################Diffrent libary -sucks for debugging
# import keyboard
# import time
# keyboard.start_recording()
# time.sleep(7)
# events = keyboard.stop_recording()
# keyboard.replay(events)




"""
import time
# Counter of pressed key

# import tkinter as tk
#
# root = tk.Tk()
#
#
# def triggered_method(param):
#     print(f"++++++++ {param} ++++++++++++")
#
#
# def key(event):
#     print(repr(event.char), repr(event.keysym), repr(event.keycode))
#     if event.char=="KP_4":
#         triggered_method("KP_4")
# root.bind("<Key>", key)
# root.mainloop()

import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from tkinter import ttk
from typing import Union, List

"""
/*-7894561230,+

Num_Lock
KP_Divide
KP_Multiply
KP_Subtract
KP_Home
Num_Lock
KP_7
KP_8
KP_9
KP_4
KP_5
KP_6
KP_1
KP_2
KP_3
KP_0
KP_Separator
KP_Enter
KP_Add
Control_L

"""


#
# events_list = []
# typed=[]
#
# def trigger_checking_sequence(listChar):
#     """
#     Determine if its double click
#     :param listChar:
#     :return:
#     """
#     print(f"Sequence {'|'.join(listChar)}")
#
#     #Typed is output display
#     if listChar[-1] ==listChar[-2]:
#         typed.append(listChar[-2])
#
#     if all(x == listChar[0] for x in listChar) and not listChar.__len__()==0:
#         print("Its doubleclick")
#     else:
#         print("Its not doubleclick")
#
#
# def add_to_event_list(input: str, target: list):
#     print(input)
#     #target.append(input)
#     global events_list
#     events_list.append(input)
#     trigger_checking_sequence(events_list)
#     if target.__len__()>2:
#         events_list.clear()
#
#
# root = tk.Tk()
# e = ttk.Entry(root)
# e.place(x=1, y=1)
# e.bind('<Key>', lambda ev: add_to_event_list(ev.keysym, events_list))
# root.mainloop()

class Key:
    values: list[str]


@dataclass
class LastKey:
    click_time: int
    value: str


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


T9 = {'.': KeypadKey.Seven, ',': KeypadKey.Seven, '!': KeypadKey.Seven, '?': KeypadKey.Seven,
      ':': KeypadKey.Seven, '-': KeypadKey.Seven, '_': KeypadKey.Seven, '\'': KeypadKey.Seven, '/': KeypadKey.Seven,
      '*': KeypadKey.Seven,
      '\\': KeypadKey.Seven, '(': KeypadKey.Seven, ')': KeypadKey.Seven, '<': KeypadKey.Seven, '>': KeypadKey.Seven,
      ';': KeypadKey.Seven, '[': KeypadKey.Seven, ']': KeypadKey.Seven,

      'a': KeypadKey.Eight, 'b': KeypadKey.Eight, 'c': KeypadKey.Eight,

      'd': KeypadKey.Nine, 'e': KeypadKey.Nine, 'f': KeypadKey.Nine,

      'g': KeypadKey.Four, 'h': KeypadKey.Four, 'i': KeypadKey.Four,

      'j': KeypadKey.Five, 'k': KeypadKey.Five, 'l': KeypadKey.Five,

      'm': KeypadKey.Six, 'n': KeypadKey.Six, 'o': KeypadKey.Six,

      'p': KeypadKey.One, 'q': KeypadKey.One, 'r': KeypadKey.One, 's': KeypadKey.One,

      't': KeypadKey.Two, 'u': KeypadKey.Two, 'v': KeypadKey.Two,

      'w': KeypadKey.Three, 'x': KeypadKey.Three, 'y': KeypadKey.Three, 'z': KeypadKey.Three,

      '0': KeypadKey.Zero,

      '1': KeypadKey.One, '2': KeypadKey.Two, '3': KeypadKey.Three,

      '4': KeypadKey.Four, '5': KeypadKey.Five, '6': KeypadKey.Six, '7': 7,

      '8': KeypadKey.Eight, '9': KeypadKey.Nine
      }

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
    # last_key: Union[None, LastKey]
    key_sequence: List[KeyboardKey]
    key_pressed_time: float

    def __init__(self):
        self.available_keys = self.get_available_keys()
        # Default value init
        self.key_pressed_time = time.time()

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

        if self.is_letter_switch(maped_key):
            maped_key.switch_letter_counter()
        self.key_sequence.append(maped_key)
        self.write_text()

    def write_text(self):
        """
        Writes actual self.key_sequence to the screen as letters
        :return: None
        """
        if self.key_sequence:
            print_value=""
            for letter in self.key_sequence:
                print_value.join(letter.value())
            print(print_value)

    def is_letter_switch(self, key: KeyboardKey) -> bool:
        """
        If detection time is less than 2 second and last keypad_button value is same as self.key_sequence[-1]
        :param key:
        :return: Bool if letter should be switched or not
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
                return self.available_keys[self.available_keys.index(available_key)]

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
