from t9keyboard.numpad_keyboard import NumpadKeyboard

if __name__ == '__main__':
    """
    Run program mainloop including keyboard listener and gui mainloop
    """
    keyboard_actions = NumpadKeyboard()
    keyboard_actions.initialize_mainloop()