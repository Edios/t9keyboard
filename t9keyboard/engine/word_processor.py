from dataclasses import dataclass, field
import time
from pathlib import Path
from typing import List, Union

import keyboard
import pyperclip


@dataclass
class Word:
    # when finished, it will be written to screen
    key_sequence: str
    word: Union[str, None] = field(default=False)
    finished: bool = field(default=False)


@dataclass
class WordProcessor:
    words: List[Word]

    def append(self, item: str):
        """
        Append key sequence to
        :param item:
        :return:
        """
        if not self.words or not self.words[-1].finished:
            self.words[-1].key_sequence.join(item)
        else:
            self.words.append(Word(key_sequence=item))

    def add_word(self, word: str):
        """
        Finish the word by changing finished parameter in word.
        Write value to the screen
        :param word: word to be written
        :return:
        """
        self.words[-1].finished = True
        self.words[-1].word = word


def delete_character(func):
    def inner(*args, **kwargs):
        keyboard.send("backspace")
        time.sleep(0.1)
        func(*args, **kwargs)

    return inner


@delete_character
def write_characters_to_screen(characters: str):
    time.sleep(0.1)
    keyboard.write(characters, delay=0.001)


def test():
    # time.sleep(4)
    print("here we go")
    keyboard.send("capslock")
    time.sleep(0.1)
    keyboard.write("kurdebele", delay=0.01)
    #time.sleep(0.1)
    keyboard.send("capslock")
    #time.sleep(0.1)
    keyboard.write("kurdebele", delay=0.01)
    # write_characters_to_screen("bele")


if __name__ == '__main__':
    time.sleep(4)
    #keyboard.write("kurdex", delay=0.1)
    #write_characters_to_screen("bele")
    pyperclip.copy("kurdebele")
    pyperclip.paste()
    """
    exbel bele
    """
