from pynput.keyboard import Controller, Key


class KeyboardWriter:
    controller: Controller

    def __init__(self):
        self.keyboard = Controller()

    def write(self, characters: str, add_space: bool = False):
        """
        Write passed character as keyboard output.
        :param add_space: If true - space character will be added on the end of written string
        :param characters: String character (or multiple) to write
        :return: None
        """
        if add_space: characters = characters + " "
        self.keyboard.type(characters)

    def backspace(self, repeat_count=1):
        """
        Sent backspace as keyboard output.
        :param repeat_count: Determine how many backspaces will be sent.
        :return: None
        """
        for _ in range(repeat_count):
            self.send(Key.backspace)

    def space(self):
        """
        Send space key.
        """
        self.send(Key.backspace)

    def send(self, key: Key):
        """
        Send keyboard key.
        :param key: Key obj to be sent
        """
        self.keyboard.tap(key)
