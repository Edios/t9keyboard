from typing import List

from t9keyboard.keyboard_keymap import numpad_character_keys_map
import tkinter as tk
import tkinter.ttk as ttk


class Gui:
    digit_buttons: List
    special_buttons: List
    actual_phrase: tk.Label
    hint_phrases: List[tk.Label]
    last_button_hover_index: int

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
root.wm_attributes("-topmost", 1)

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


# Layout Frames
actual_phrase_labels_frame = tk.LabelFrame(root, text="Actual phrase", padx=20, pady=5)
actual_phrase_labels_frame.grid(row=0, column=0)

available_phrases_labels_frame = tk.LabelFrame(root, text="Available phrases", padx=20, pady=5, )
available_phrases_labels_frame.grid(row=1, column=0)

digit_buttons_frame = tk.LabelFrame(root, text="Digit keys", padx=20, pady=20)
digit_buttons_frame.grid(row=2, column=0)

special_buttons_frame = tk.LabelFrame(root, text="Special keys", padx=20, pady=20)
special_buttons_frame.grid(row=3, column=0)

digit_labels_table = digit_rows(numpad_character_keys_map)

# Default button styling
style = ttk.Style(digit_buttons_frame)
style.configure('TButton', font=('Arial', 9))
style.configure('TLabel', font=('Arial', 9))
# TODO:Store gui elements in object

# offset_digit_buttons=len(digit_labels_table)+actual_label_rows_number
# Actual phrase label
actual_phrase = tk.Label(actual_phrase_labels_frame, text="Choosed", font=('Arial', 14))
actual_phrase.grid(row=0, column=1, padx=20, pady=5)

# Available phrases

# Hin
available_phrases=[]
for col in range(5):
    hint_phrase = tk.Label(available_phrases_labels_frame, text="Phrase", font=('Arial', 10, 'normal'))
    hint_phrase.grid(row=0, column=col, padx=20, pady=5)
    available_phrases.append(hint_phrase)

# hint_phrase_1 = tk.Label(available_phrases_labels_frame, text="Okoń", font=('Arial', 11, 'bold'), bg="#a4aab3",
#                          fg="#ffffff")
# hint_phrase_1.grid(row=0, column=0, padx=20, pady=5)
# hint_phrase_2 = tk.Label(available_phrases_labels_frame, text="Phrase", font=('Arial', 10, 'normal'))
# hint_phrase_2.grid(row=0, column=1, padx=20, pady=5)
# hint_phrase_3 = tk.Label(available_phrases_labels_frame, text="Phrase", font=('Arial', 10, 'normal'))
# hint_phrase_3.grid(row=0, column=2, padx=20, pady=5)
# hint_phrase_4 = tk.Label(available_phrases_labels_frame, text="Phrase", font=('Arial', 10, 'normal'))
# hint_phrase_4.grid(row=0, column=3, padx=20, pady=5)
# hint_phrase_5 = tk.Label(available_phrases_labels_frame, text="Phrase", font=('Arial', 10, 'normal'))
# hint_phrase_5.grid(row=0, column=4, padx=20, pady=5)

# Buttons
digit_keys = []
for row in range(len(digit_labels_table)):
    for col in range(len(digit_labels_table[row])):
        i = digit_labels_table[row][col]
        b = tk.Button(digit_buttons_frame, text=str(i), state=tk.DISABLED, width=5, font=('Arial', 12))
        b.grid(row=row + 1, column=col, padx=5, pady=5)
        digit_keys.append(b)

# Special Buttons
switch_actual_phrase_button = tk.Button(special_buttons_frame, text=".", state=tk.DISABLED, width=5,
                                        font=('Arial', 11, "bold"))
switch_actual_phrase_button.grid(row=1, column=0, padx=5, pady=5)

switch_actual_phrase_label = tk.Label(special_buttons_frame, text="Switch actual phrase", font=('Arial', 10, 'normal'))
switch_actual_phrase_label.grid(row=1, column=1, padx=5, pady=5)

backspace_button = tk.Button(special_buttons_frame, text="+", state=tk.DISABLED, width=5, font=('Arial', 12))
backspace_button.grid(row=2, column=0, padx=5, pady=5)

backspace_label = tk.Label(special_buttons_frame, text="Backspace", font=('Arial', 10, 'normal'))
backspace_label.grid(row=2, column=1, padx=5, pady=5)

# method for applying style
change_hoover_button_state(digit_keys[0])
root.mainloop()
