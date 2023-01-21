from pynput import keyboard

def keyboard_listener():
    global key
    global keyboard_listener

    def on_press(key):
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            print('You entered a number from the numpad: ', key.char)
        else:
            print('normal key', key)

    def on_release(key):
        print('on release', key)
        if key == keyboard.Key.esc:
            return False

    def win32_event_filter(msg, data):
        #if(msg == 257 or msg == 256) and (data.vkCode == 38 or data.vkCode == 40):
        if hasattr(data, 'vkCode') and 96 <= data.vkCode <= 105:
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