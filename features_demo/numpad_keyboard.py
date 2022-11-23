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


class Keypad(Enum):
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


T9 = {'.': Keypad.Seven, ',': Keypad.Seven, '!': Keypad.Seven, '?': Keypad.Seven,
      ':': Keypad.Seven, '-': Keypad.Seven, '_': Keypad.Seven, '\'': Keypad.Seven, '/': Keypad.Seven, '*': Keypad.Seven,
      '\\': Keypad.Seven, '(': Keypad.Seven, ')': Keypad.Seven, '<': Keypad.Seven, '>': Keypad.Seven,
      ';': Keypad.Seven, '[': Keypad.Seven, ']': Keypad.Seven,

      'a': Keypad.Eight, 'b': Keypad.Eight, 'c': Keypad.Eight,

      'd': Keypad.Nine, 'e': Keypad.Nine, 'f': Keypad.Nine,

      'g': Keypad.Four, 'h': Keypad.Four, 'i': Keypad.Four,

      'j': Keypad.Five, 'k': Keypad.Five, 'l': Keypad.Five,

      'm': Keypad.Six, 'n': Keypad.Six, 'o': Keypad.Six,

      'p': Keypad.One, 'q': Keypad.One, 'r': Keypad.One, 's': Keypad.One,

      't': Keypad.Two, 'u': Keypad.Two, 'v': Keypad.Two,

      'w': Keypad.Three, 'x': Keypad.Three, 'y': Keypad.Three, 'z': Keypad.Three,

      '0': Keypad.Zero,

      '1': Keypad.One, '2': Keypad.Two, '3': Keypad.Three,

      '4': Keypad.Four, '5': Keypad.Five, '6': Keypad.Six, '7': 7,

      '8': Keypad.Eight, '9': Keypad.Nine
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
    keypad_number: Keypad
    letters: List[str]
    letter_counter: int = field(default=0)

    def value(self)->str:
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
        if self.letter_counter < len(self.letters):
            self.letter_counter += 1
        else:
            self.letter_counter = 0


class KeyboardActions:
    available_keys: List[KeyboardKey]
    # last_key: Union[None, LastKey]
    key_sequence: List[KeyboardKey]

    def __init__(self):
        self.available_keys = self.get_available_keys()

    def handle_keypress(self, keypad_button: Keypad):
        """
        Add value to self.key_sequence list
        Uses:
            self.key_sequence
            self.last_key_time

        If detection time is less than 1.5 second = consider it as switch_letter
        If detection time is over 1.5 second = consider it as add_letter
        :param keypad_button: Keypad(Enum) Pressed Keypad Key
        :return:
        """
        maped_key = self.map_key(keypad_button)

        if self.is_letter_switch(keypad_button):
            self.switch_letter(maped_key)
        if keypad_button == "num 5":
            print("num 5 pressed")
            self.last_key = LastKey(1, "num 5")
        elif keypad_button == "num 0":
            self.last_key = LastKey(1, "space")
            print("Space cleared text")
        else:
            print("Its diffrent key")

        self.write_text()

    def write_text(self):
        """
        Writes actual self.key_sequence to the screen as letters
        :return:
        """
        pass

    def is_letter_switch(self, keypad_button: Keypad):
        """
        If detection time is less than 1.5 second and last keypad_button value is same as self.key_sequence[-1]
        :param keypad_button:
        :return:
        """
        pass

    def map_key(self, key: Keypad) -> KeyboardKey:
        """
        Map key to object
        :param key: Keypad
        :return:
        """
        pass

    def switch_letter(self, maped_key):
        pass

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
            # TODO: if Value == Keypad.Value Map all keys as KeyboardKey(value,[key,key,key])
            try:
                attribute = getattr(Keypad, key)
                available_keys.append(KeyboardKey(attribute, values))
            except AttributeError:
                # TODO: Remove print
                print("Could not match character with keypad ")
        return available_keys


import keyboard

# def handle_key(key):
#     print(key)


keyboard_actions = KeyboardActions()

keyboard.add_hotkey('num 9', keyboard_actions.handle_keypress, args=[Keypad.Nine])
keyboard.add_hotkey('num 8', keyboard_actions.handle_keypress, args=[Keypad.Eight])
keyboard.add_hotkey('num 7', keyboard_actions.handle_keypress, args=[Keypad.Seven])
keyboard.add_hotkey('num 6', keyboard_actions.handle_keypress, args=[Keypad.Six])
keyboard.add_hotkey('num 5', keyboard_actions.handle_keypress, args=[Keypad.Five])
keyboard.add_hotkey('num 4', keyboard_actions.handle_keypress, args=[Keypad.Four])
keyboard.add_hotkey('num 3', keyboard_actions.handle_keypress, args=[Keypad.Three])
keyboard.add_hotkey('num 2', keyboard_actions.handle_keypress, args=[Keypad.Two])
keyboard.add_hotkey('num 1', keyboard_actions.handle_keypress, args=[Keypad.One])
keyboard.add_hotkey('num 0', keyboard_actions.handle_keypress, args=[Keypad.Zero])
