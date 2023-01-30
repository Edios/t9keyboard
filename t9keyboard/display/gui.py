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
    highlighted_phrase_label_index: Union[int, None] = field(default=None)

    def __post_init__(self):
        self._create_widgets()

        # TODO: This section can be converted to unit test with checking element properties (element.cget())
        # Button Test
        # self.switch_button_highlight(4)
        # self.switch_button_highlight(2)
        # self.switch_button_highlight(6)
        # self.switch_button_highlight(2,is_special_button=True)
        # self.switch_button_highlight(6)

        # # Label Test
        # self.switch_phrases_highlighted_element(2)
        # self.switch_phrases_highlighted_element(1)
        #
        # # Actual phrase Test
        # self.update_actual_phrase('okay')
        #
        # #Available phrases Test
        # test1=['Buddy','okay','Go','Abra','Kadabra']
        # self.update_available_phrases(test1)
        # test2 = ['okay','Buddy', 'Gotta']
        # self.switch_phrases_highlighted_element(0)
        # self.update_available_phrases(test2)

    def initialize_mainloop(self):
        """
        Add windows parameters and then initialize mainloop of Tk.
        """
        self.root.wm_attributes("-topmost", 1)
        self.root.title("T9 Numeric pad keyboard")
        self.root.resizable(False, False)
        self.root.geometry("500x550")
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

        self.highlighted_special_button_index = None
        self.highlighted_special_button_index = None

    def update_actual_phrase(self, word: str):
        self.actual_phrase.config(text=word)

    def update_available_phrases(self, phrases: List[str]):
        if phrases.__len__() < self.available_phrases.__len__():
            differance = self.available_phrases.__len__() - phrases.__len__()
            for _ in range(differance):
                phrases.append("        ")
        for counter, phrase in enumerate(phrases):
            self._change_phrase_label_text(phrase, counter)

    def _change_phrase_label_text(self, label_text: str, label_index: int):
        self.available_phrases[label_index].config(text=label_text)

    def switch_phrases_highlighted_element(self, label_index):
        if self.highlighted_phrase_label_index:
            self._remove_label_highlight()
        self._change_label_highlight(label_index)
        self.highlighted_phrase_label_index = label_index

    def _change_label_highlight(self, label_index: int, highlight=True):
        self.available_phrases[label_index].config(**self.get_label_styles(highlight=highlight))

    def _remove_label_highlight(self):
        if self.highlighted_phrase_label_index:
            self._change_label_highlight(self.highlighted_phrase_label_index, highlight=False)

    @staticmethod
    def get_button_styles(highlight: bool = False) -> dict:
        """
        Get styles for button.
        Intention for this class is to feed object button as kwargs:
            Usage:
                Button(root,**get_button_styles())
        :param highlight: Choose if method should return style for highlighted button
        """
        default_button = {
            "disabledforeground": "#333333",
            "bg": "#ffffff",
            "state": tk.DISABLED,
            "width": 5,
            "font": ('Arial', 12)
        }
        highlight_button = {
            "fg": "#ffffff",
            "bg": "#333333"
        }
        return highlight_button if highlight else default_button

    @staticmethod
    def get_label_styles(highlight: bool = False) -> dict:
        """
        Get styles for Label.
        Intention for this class is to feed object button as kwargs:
            Usage:
                Label(root,**get_button_styles())
        :param highlight: Choose if method should return style for highlighted label
        """
        default_label = {
            "font": ('Arial', 11),
            "bg": "SystemButtonFace",
            "fg": "#000000"
        }
        highlight_label = {
            "fg": "#ffffff",
            "bg": "#333333"
        }
        return highlight_label if highlight else default_label

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
            available_phrase = tk.Label(available_phrases_labels_frame, text="Phrase", **self.get_label_styles(),
                                        padx=5, pady=5, )
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
                               **self.get_label_styles())
        space_label.grid(row=0, column=1, padx=5, pady=5)
        # Switch actual phrase
        switch_actual_phrase_button = tk.Button(special_buttons_frame, text=",", **self.get_button_styles())
        switch_actual_phrase_button.grid(row=1, column=0, padx=5, pady=5)
        self.special_buttons.append(switch_actual_phrase_button)

        switch_actual_phrase_label = tk.Label(special_buttons_frame, text="Switch actual phrase",
                                              **self.get_label_styles())
        switch_actual_phrase_label.grid(row=1, column=1, padx=5, pady=5)
        # Backspace
        backspace_button = tk.Button(special_buttons_frame, text="+", **self.get_button_styles())
        backspace_button.grid(row=2, column=0, padx=5, pady=5)
        self.special_buttons.append(backspace_button)

        backspace_label = tk.Label(special_buttons_frame, text="Backspace", **self.get_label_styles())
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
