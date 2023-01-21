from enum import Enum
#This is key map for keyboard libary
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
    'enter': ['enter'],
    'num lock':['num lock']
}

#This is key map for pynput libary
#Source for Virtual-Key Codes: https://cherrytree.at/misc/vk.htm
virtual_key_to_alphabet_keys_map = {
    '103': ['.', ',', '?', '!'],
    '104': ['a', 'b', 'c'],
    '105': ['d', 'e', 'f'],
    '100': ['g', 'h', 'i'],
    '101': ['j', 'k', 'l'],
    '102': ['m', 'n', 'o'],
    '97': ['p', 'q', 'r', 's'],
    '98': ['t', 'u', 'v'],
    '99': ['w', 'x', 'y', 'z']
}
virtual_key_to_special_keys_map = {
    '96': ['space'],
    '107': ['backspace'],
    '109': ['switch_keyboard_mode'],
    '110': ['switch_letter'],
    '144':['num lock']
    #enter key could not be easily determined
    #'enter': ['enter'],
}
class SpecialAction(Enum):
    backspace = "backspace"
    switch_keyboard_mode = "switch_keyboard_mode"
    switch_letter = "switch_letter"
    space = "space"
