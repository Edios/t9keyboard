from enum import Enum, auto
from pynput.keyboard import KeyCode

from t9keyboard.display.gui import Gui
from t9keyboard.engine.numpad_listener import numpad_listener
from t9keyboard.keyboard_keymap import numpad_key_to_virtual_key_code_map
from t9keyboard.single_tap_keyboard_mode import SingleTapMode
from t9keyboard.t9_mode import T9Mode


class NumpadKeyboardMode(Enum):
    single_tap = auto()
    t9 = auto()


class NumpadKeyboard:
    gui:Gui
    keyboard_mode: NumpadKeyboardMode
    single_tap_mode: SingleTapMode
    t9_mode: T9Mode

    def __init__(self):
        self.gui=Gui()
        # Default keyboard mode set to T9
        self.keyboard_mode = NumpadKeyboardMode.t9
        self.t9_mode = T9Mode(self.gui)
        # load single tap mode
        self.single_tap_mode = SingleTapMode()

    def initialize_mainloop(self):
        """
        Initialize keyboard listener and gui mainloop
        :return:
        """
        listener = numpad_listener(self.on_press_reaction)
        self.gui.initialize_mainloop()
        listener.stop()

    def on_press_reaction(self, keypad_button: KeyCode):
        """
        This method should be triggered by method which is detecting numeric keypad button presses.
        :param keypad_button: KeyboardEvent Pressed Keypad Key
        :return: None
        """
        button = self.map_virtual_key_to_known_button(str(keypad_button.vk))
        if self.keyboard_mode == NumpadKeyboardMode.single_tap:
            mapped_key = self.single_tap_mode.map_key(button)
            self.single_tap_mode.handle_single_tap_mode(mapped_key)
        if self.keyboard_mode == NumpadKeyboardMode.t9:
            mapped_key = self.t9_mode.map_key(button)
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

    @staticmethod
    def map_virtual_key_to_known_button(key: str) -> str:
        """
        Convert Virtual-Key Code to numpad character
        :return: Known button from map
        """
        if key in numpad_key_to_virtual_key_code_map.keys():
            return numpad_key_to_virtual_key_code_map[key]
        raise Exception(f"Key not found in known buttons map: {key}")