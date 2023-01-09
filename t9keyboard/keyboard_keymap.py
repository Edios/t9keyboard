from enum import Enum

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
    '.': ['switch_letter'],
    'enter': ['enter']
}


class SpecialAction(Enum):
    backspace = "backspace"
    switch_keyboard_mode = "switch_keyboard_mode"
    switch_letter = "switch_letter"
    space = "space"
