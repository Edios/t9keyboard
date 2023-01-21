from enum import Enum, auto
from pathlib import Path

import keyboard
from keyboard import KeyboardEvent
from pynput.keyboard import KeyCode

from t9keyboard.engine.pynput_poc import numpad_listner
from t9keyboard.t9_mode import T9Mode
from t9keyboard.single_tap_keyboard_mode import SingleTapMode
from t9keyboard.t9_mode import T9Mode


# TODO: Print this graphics as helper


class NumpadKeyboardMode(Enum):
    single_tap = auto()
    t9 = auto()


class NumpadKeyboard:
    keyboard_mode: NumpadKeyboardMode

    single_tap_mode: SingleTapMode
    t9_mode: T9Mode

    def __init__(self):
        # Default keyboard mode
        self.keyboard_mode = NumpadKeyboardMode.t9
        self.t9_mode = T9Mode()

        # load single tap mode
        self.single_tap_mode = SingleTapMode()

    def on_press_reaction(self, keypad_button: KeyCode):
        """
        This method should be triggered by keyboard.on_press which produces KeyboardEvent.
        :param keypad_button: KeyboardEvent Pressed Keypad Key
        :return: None
        """

        if self.keyboard_mode == NumpadKeyboardMode.single_tap:
            mapped_key = self.single_tap_mode.map_key(keypad_button.vk)
            self.single_tap_mode.handle_single_press_mode(mapped_key)
        if self.keyboard_mode == NumpadKeyboardMode.t9:
            mapped_key = self.t9_mode.map_key(keypad_button.vk)
            self.t9_mode.handle_t9_mode(mapped_key)

    def switch_keyboard_mode(self):
        """
        Based on current value of keyboard mode change it to one which is not set.
        :return: None
        """
        match self.keyboard_mode:
            case NumpadKeyboardMode.t9:
                self.keyboard_mode = NumpadKeyboardMode.single_tap
            case NumpadKeyboardMode.single_tap:
                self.keyboard_mode = NumpadKeyboardMode.t9


if __name__ == '__main__':
    keyboard_actions = NumpadKeyboard()

    #keyboard.on_press(keyboard_actions.on_press_reaction)
    numpad_listner(keyboard_actions.on_press_reaction)
