from pynput import keyboard
from pynput.keyboard import KeyCode

from t9keyboard.keyboard_keymap import virtual_key_to_alphabet_keys_map, virtual_key_to_special_keys_map


def is_numpad_key(vk_code:int)->bool:
    """
    Check if given key is Numeric Keypad keyboard key by comparing his vk param.
    Use key map key's which are Virtual-Key Codes.
    """
    numpad_virtual_key_codes=[int(key_code) for key_code in list(virtual_key_to_alphabet_keys_map.keys())+list(virtual_key_to_special_keys_map.keys())]
    return True if vk_code in numpad_virtual_key_codes else False
def keyboard_listener():
    global key
    global keyboard_listener

    def on_press(key):
        if hasattr(key, 'vk') and is_numpad_key(key.vk):
            print('You entered a number from the numpad: ', key.vk)
        else:
            print('normal key', key)

    def on_release(key):
        print('on release', key)
        if key == keyboard.Key.esc:
            return False

    def win32_event_filter(_, data):
        #if(msg == 257 or msg == 256) and (data.vkCode == 38 or data.vkCode == 40):
        if hasattr(data, 'vkCode') and is_numpad_key(data.vkCode):
            listener._suppress = True
        else:
            listener._suppress = False
        return True

    #it suppress only numpad
    return  keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        win32_event_filter=win32_event_filter,
        suppress=True
    )


listener = keyboard_listener()

if __name__== '__main__':
    with listener as ml:
        ml.join()