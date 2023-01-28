from typing import List

from t9keyboard.keyboard_keymap import numpad_character_keys_map
import tkinter as tk
import tkinter.ttk as ttk


class Gui:
    digit_buttons: List
    special_buttons: List
    actual_phrase: tk.Label
    hint_phrases:List[tk.Label]
    def switch_hoover(self):
        pass

    def update_actual_phrase(self):
        pass

    def update_phrase_hints(self):
        pass


class GuiEngine:
    # could be method
    pass


root = tk.Tk()


def digit_rows(keys_map: dict, row_length: int = 3) -> List[List[str]]:
    """
    Take keymap dictionary, split it into 3x3 structure where each list contains label for button.
    Label for button is a string which glue together 'key+newline+values separated by space'.
    Structure:
    [
        ['7\n . ? !','8\n a b c','9\n d e f'],
        ['row2','row2','row2'],
        ['row3','row3','row3']
    ]

    :param row_length: Maximum row length
    :param keys_map: dictionary with keymap where key is digit and value is list of string characters
    :return: List of rows
    """
    list_of_rows = []
    key_labels = create_key_labels(keys_map)
    for i in range(0, len(key_labels), row_length):
        list_of_rows.append(key_labels[i:i + row_length])
    return list_of_rows


def create_key_labels(keys: dict) -> List[str]:
    """
    Create label for button
    Label for button is a string which glue together 'key+newline+values separated by space'.
    :param keys:
    :return:
    """
    key_labels = []
    for key, value in keys.items():
        key_labels.append(f"{key}\n{' '.join(value)}")
    return key_labels


def change_hoover_button_state(button: tk.Button):
    # button.config(bg=f'#{randrange(100000, 666666)}', fg='blue')
    # button.config(style='hovered.TButton')
    # button.config(bg=f'#{randrange(100000, 666666)}', fg='blue')
    button.config(bg='blue')


# Layout for Numpad
btns_frame = tk.Frame(root, padding=10)
btns_frame.pack()
digit_labels_table = digit_rows(numpad_character_keys_map)

# Default button styling
style = ttk.Style(btns_frame)
style.configure('TButton', font=('Arial', 9))
# TODO:Store gui elements in object
digit_keys = []

for row in range(len(digit_labels_table)):
    for col in range(len(digit_labels_table[row])):
        i = digit_labels_table[row][col]
        b = tk.Button(btns_frame, text=str(i), state=tkinter.DISABLED, width=5, font=('Arial', 12))
        b.grid(row=row + 1, column=col, padx=5, pady=5)
        digit_keys.append(b)
change_hoover_button_state(digit_keys[0])
root.mainloop()
