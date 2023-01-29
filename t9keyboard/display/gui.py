from dataclasses import dataclass, field
from typing import List, Union

from t9keyboard.keyboard_keymap import numpad_character_keys_map
import tkinter as tk
import tkinter.ttk as ttk


@dataclass
class Gui:
    root: tk.Tk = tk.Tk()

    digit_buttons: List[tk.Button] = field(default_factory=list)
    special_buttons: List[tk.Button] = field(default_factory=list)
    actual_phrase: tk.Label = field(default=tk.Label)
    available_phrases: List[tk.Label] = field(default_factory=list)

    highlighted_digit_button_index: Union[int, None] = field(default=None)
    highlighted_special_button_index: Union[int, None] = field(default=None)

    def __post_init__(self):
        self._create_widgets()
        self.switch_button_highlight(4)
        self.switch_button_highlight(2)
        self.switch_button_highlight(6)
        self.switch_button_highlight(2,is_special_button=True)
        self.switch_button_highlight(6)



    def initialize_mainloop(self):
        """
        Add always on-top, title and then initialize mainloop of Tk.
        """
        self.root.wm_attributes("-topmost", 1)
        self.root.title("T9 Numeric pad keyboard")
        self.root.resizable(False, False)
        self.root.mainloop()

    def switch_button_highlight(self, button_index, is_special_button=False):
        if self.highlighted_digit_button_index or self.highlighted_special_button_index:
            self._remove_button_hover()
        if is_special_button:
            self._change_button_highlight(button_index, self.special_buttons)
            self.highlighted_special_button_index = button_index
        else:
            self._change_button_highlight(button_index, self.digit_buttons)
            self.highlighted_digit_button_index = button_index

    def _change_button_highlight(self, button_index, button_list, highlight=True):
        button_list[button_index].config(**self.get_button_styles(highlight=highlight))

    def _remove_button_hover(self):
        if self.highlighted_special_button_index:
            self._change_button_highlight(self.highlighted_special_button_index, self.special_buttons, highlight=False)
        if self.highlighted_digit_button_index:
            self._change_button_highlight(self.highlighted_digit_button_index, self.digit_buttons, highlight=False)

        self.highlighted_special_button_index=None
        self.highlighted_special_button_index=None

    def update_actual_phrase(self):
        pass

    def update_available_phrases(self):
        pass

    def update_available_phrases_chosen_element(self):
        # TODO: Apply font=('Arial', 11, 'bold'), bg="#a4aab3",fg="#ffffff" for actually choosed phrase
        pass

    def _apply_label_highlight(self):
        pass

    def _remove_label_highlight(self):
        pass

    @staticmethod
    def get_button_styles(highlight: bool = False) -> dict:
        default_button = {
            "disabledforeground": "#333333",
            "bg": "#ffffff",
            "state": tk.DISABLED,
            "width": 5,
            "font": ('Arial', 12)
        }
        highlight_button = {
            "disabledforeground": "#ffffff",
            "bg": "#333333"
        }
        return highlight_button if highlight else default_button

    def _create_widgets(self):
        """
        Method for creating all tkinter UI elements.
        First create frames, then fill them up with labels and buttons.
        Accessible widgets will be stored in proper class fields.

        Class fields which would be filled:
            digit_buttons: List[tk.Button]
            special_buttons: List[tk.Button]
            actual_phrase: tk.Label
            available_phrases: List[tk.Label]
        """
        # Layout Frames
        actual_phrase_labels_frame = tk.LabelFrame(self.root, text="Actual phrase", padx=20, pady=5)
        actual_phrase_labels_frame.grid(row=0, column=0)

        available_phrases_labels_frame = tk.LabelFrame(self.root, text="Available phrases", padx=20, pady=5, )
        available_phrases_labels_frame.grid(row=1, column=0)

        digit_buttons_frame = tk.LabelFrame(self.root, text="Digit keys", padx=20, pady=20)
        digit_buttons_frame.grid(row=2, column=0)

        special_buttons_frame = tk.LabelFrame(self.root, text="Special keys", padx=20, pady=20)
        special_buttons_frame.grid(row=3, column=0)

        # Actual phrase label
        actual_phrase = tk.Label(actual_phrase_labels_frame, text="Chosen", font=('Arial', 14))
        actual_phrase.grid(row=0, column=1, padx=20, pady=5)
        self.actual_phrase = actual_phrase

        # Available phrases
        for col in range(5):
            available_phrase = tk.Label(available_phrases_labels_frame, text="Phrase", font=('Arial', 10, 'normal'))
            available_phrase.grid(row=0, column=col, padx=20, pady=5)
            self.available_phrases.append(available_phrase)

        # Digit buttons
        digit_labels_table = create_digit_rows_from_keymap(numpad_character_keys_map)
        for row in range(len(digit_labels_table)):
            for col in range(len(digit_labels_table[row])):
                i = digit_labels_table[row][col]
                digit_button = tk.Button(digit_buttons_frame, text=str(i), **self.get_button_styles())
                digit_button.grid(row=row + 1, column=col, padx=5, pady=5)
                self.digit_buttons.append(digit_button)

        # Special Buttons

        # Space
        space_button = tk.Button(special_buttons_frame, text="0", **self.get_button_styles())
        space_button.grid(row=0, column=0, padx=5, pady=5)
        self.special_buttons.append(space_button)

        space_label = tk.Label(special_buttons_frame, text="Space / Accept word",
                               font=('Arial', 10, 'normal'))
        space_label.grid(row=0, column=1, padx=5, pady=5)
        # Switch actual phrase
        switch_actual_phrase_button = tk.Button(special_buttons_frame, text=",",**self.get_button_styles())
        switch_actual_phrase_button.grid(row=1, column=0, padx=5, pady=5)
        self.special_buttons.append(switch_actual_phrase_button)

        switch_actual_phrase_label = tk.Label(special_buttons_frame, text="Switch actual phrase",
                                              font=('Arial', 10, 'normal'))
        switch_actual_phrase_label.grid(row=1, column=1, padx=5, pady=5)
        # Backspace
        backspace_button = tk.Button(special_buttons_frame, text="+",**self.get_button_styles())
        backspace_button.grid(row=2, column=0, padx=5, pady=5)
        self.special_buttons.append(backspace_button)

        backspace_label = tk.Label(special_buttons_frame, text="Backspace", font=('Arial', 10, 'normal'))
        backspace_label.grid(row=2, column=1, padx=5, pady=5)


def create_digit_rows_from_keymap(keys_map: dict, row_length: int = 3) -> List[List[str]]:
    """
    Helper method for GUI.
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
    Helper method for GUI.
    Create label for button.
    Button label is a string which glue together 'key+newline+values separated by space'.
    :param keys:
    :return:
    """
    key_labels = []
    for key, value in keys.items():
        key_labels.append(f"{key}\n{' '.join(value)}")
    return key_labels


# def change_hoover_button_state(button: tk.Button):
#     # button.config(bg=f'#{randrange(100000, 666666)}', fg='blue')
#     # button.config(style='hovered.TButton')
#     # button.config(bg=f'#{randrange(100000, 666666)}', fg='blue')
#     button.config(bg='blue')


# Default button styling
# style = ttk.Style(digit_buttons_frame)
# style.configure('TButton', font=('Arial', 9))
# style.configure('TLabel', font=('Arial', 9))
gui = Gui()
gui.initialize_mainloop()
# method for applying style
# change_hoover_button_state(digit_keys[0])
