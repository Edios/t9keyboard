from typing import Union

from pynput import keyboard
from pynput.keyboard import KeyCode

from t9keyboard.keyboard_keymap import numpad_key_to_virtual_key_code_map


def is_numpad_key(vk_code: Union[int, str]) -> bool:
    """
    Determine if given input is numeric keypad corresponding virtual-key code.
    Use key map key's which are Virtual-Key Codes.
    """
    numpad_virtual_key_codes = [int(key_code) for key_code in list(numpad_key_to_virtual_key_code_map.keys())]
    return True if vk_code in numpad_virtual_key_codes else False


def keyboard_listener(handled_method=None):
    global key
    global keyboard_listener

    def on_press(key):
        if hasattr(key, 'vk') and is_numpad_key(key.vk):
            if handled_method:
                handled_method(key)

    def on_release(key):
        # print('on release', key)
        if key == keyboard.Key.esc:
            return False

    def win32_event_filter(_, data):
        if hasattr(data, 'vkCode') and is_numpad_key(data.vkCode):
            listener._suppress = True
        else:
            listener._suppress = False
        return True

    # it suppress only numpad
    return keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        win32_event_filter=win32_event_filter,
        suppress=True
    )


def method_to_handle(key: KeyCode):
    print(f"Method got: {key.vk} {key}")


def numpad_listener(handled_method):
    global listener
    listener = keyboard_listener(handled_method=handled_method)
    with listener as ml:
        ml.join()
# TODO: method_to_handle can be used to test this piece of code
# numpad_listner(method_to_handle)
