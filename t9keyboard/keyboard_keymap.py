from enum import Enum

# This is key map for keyboard libary
numpad_character_keys_map = {
    '7': ['.', ',', '?', '!'],
    '8': ['a', 'b', 'c'],
    '9': ['d', 'e', 'f'],
    '4': ['g', 'h', 'i'],
    '5': ['j', 'k', 'l'],
    '6': ['m', 'n', 'o'],
    '1': ['p', 'q', 'r', 's'],
    '2': ['t', 'u', 'v'],
    '3': ['w', 'x', 'y', 'z']
}
numpad_keyboard_special_keys_map = {
    '0': ['space'],
    '+': ['backspace'],
    '-': ['switch_keyboard_mode'],
    ',': ['switch_letter'],
    'enter': ['enter'],
    'num lock': ['num lock']
}

# This is key map for pynput libary
# Source for Virtual-Key Codes: https://cherrytree.at/misc/vk.htm
numpad_key_to_virtual_key_code_map = {
    '103': "7",
    '104': "8",
    '105': "9",
    '100': "4",
    '101': "5",
    '102': "6",
    '97': "1",
    '98': "2",
    '99': "3",
    '96': "0",
    '107': '+',
    '109': '-',
    '110': ',',
    '144': 'num lock'
}


class SpecialAction(Enum):
    backspace = "backspace"
    switch_keyboard_mode = "switch_keyboard_mode"
    switch_letter = "switch_letter"
    space = "space"
    seven = "."
