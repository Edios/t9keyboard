import os

import pytest
from pynput.keyboard import KeyCode

"""
on_press_reaction
1. Check if it calls t9 mode with correct key value (but first change self.keyboard_mode value)
2. Check if it calls single tap mode (but first change self.keyboard_mode value)

switch_keyboard_mode
3. Switch_keyboard_mode - is switching correctly? - can make 2 tc from it

map_virtual_key_to_known_button
4. Convert Virtual-Key Code to its 'digit' value.
"""
from t9keyboard.numpad_keyboard import NumpadKeyboard

# Change dir to match default dict patch
os.chdir("../t9keyboard")
keyboard_actions = NumpadKeyboard()


def test_t9_trigger(mocker):
    t9 = mocker.patch("t9keyboard.t9_mode.T9Mode.handle_t9_mode")
    keyboard_actions.on_press_reaction(KeyCode(vk="101"))
    assert t9.call_count == 1
