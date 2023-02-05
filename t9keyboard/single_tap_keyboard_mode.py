import copy
import datetime
import time
from dataclasses import dataclass, field
from typing import List

import keyboard

from t9keyboard.engine.keyboard_writer import KeyboardWriter
from t9keyboard.keyboard_keymap import numpad_character_keys_map, numpad_keyboard_special_keys_map, SpecialAction


@dataclass
class SingleTapKey:
    keypad_button: str
    letters: List[str]
    is_special_key: bool = field(default=False)
    letter_counter: int = field(default=0)
    switched_letter_value: bool = field(default=False)
    pressed_time: datetime = field(default_factory=datetime.datetime.now)

    # def __post_init__(self):
    #     self.is_special_key = True if len(self.letters) < 2 else False

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


class SingleTapMode:
    available_keys: List[SingleTapKey]
    key_sequence: List[SingleTapKey]
    key_pressed_time: datetime
    writer:KeyboardWriter

    def __init__(self):
        self.available_keys = self.get_available_keyboard_keys()
        # Default value init
        self.key_sequence = []
        self.writer=KeyboardWriter()

    def map_key(self, key: str) -> SingleTapKey:
        """
        Map key from input to object of from list of available keyboard buttons.
        KeyboardKey object add information about letters values which will be used to perform logic.

        :param key: str Value which represents pressed key
        :return: Matching SingleTapKey from available keys
        """
        for index,available_key in enumerate(self.available_keys):
            if key == available_key.keypad_button:
                new_key_object = copy.deepcopy(self.available_keys[index])
                # Default object timestamp need to be refreshed
                new_key_object.refresh_timestamp()
                return new_key_object
        raise Exception(f"Could not find {key} in available_keys.")

    @staticmethod
    def get_available_keyboard_keys() -> List[SingleTapKey]:
        """
        Return list of SingleTapKey objects. Need dict with single_tap_keyboard_character_map.
        :return: List of available KeyboardKey objects
        """
        available_keys = []
        for key, values in numpad_character_keys_map.items():
            available_keys.append(SingleTapKey(key, values))
        for key, values in numpad_keyboard_special_keys_map.items():
            available_keys.append(SingleTapKey(key, values, is_special_key=True))
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

    def handle_single_tap_mode(self, mapped_key: SingleTapKey):
        """
        #TODO: Add method description
        :param mapped_key:
        :return:
        """
        if mapped_key.is_special_key:
            # TODO: Handle special action
            self.perform_special_key_action(mapped_key)
        elif self.is_letter_switch(mapped_key):
            self.key_sequence[-1].switch_letter_counter()
            self.write_switched_text_from_key(self.key_sequence[-1].value())
        else:
            self.key_sequence.append(mapped_key)
            self.writer.write(mapped_key.value())

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
        # WA: Delete previous character by sending backspace
        self.writer.backspace()
        time.sleep(0.01)
        self.writer.write(character)

    def is_letter_switch(self, key: SingleTapKey) -> bool:
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

    def perform_special_key_action(self, mapped_key):
        # WARNING: This requires python >3.10 (case matching method)
        action = getattr(SpecialAction, mapped_key.value())
        match action:
            case SpecialAction.backspace:
                self.writer.backspace()
            case SpecialAction.switch_keyboard_mode:
                # self.switch_keyboard_mode()
                pass
