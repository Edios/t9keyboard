from dataclasses import dataclass, field
from typing import List


@dataclass
class WordProcessor:
    finished_words: List[str] = field(default=list)
    queued_word: str = field(default="")

    def append_characters(self, characters: str):
        """
        Append character (or multiple) to queued_word.
        :param characters: string to be added into queued_word
        """
        self.queued_word += characters

    def remove_last_finished_word(self):
        """
        Remove last element from finished_words list.
        :return:
        """
        self.finished_words.pop()

    def finish_word(self):
        """
        Append actual queued_word value to finished_words. Clear queued_word.
        :return: None
        """
        self.finished_words.extend(self.queued_word)
        self.clear_queued_word()

    def get_words(self, slicing: slice = slice(0, None)) -> str:
        """
        Method for pulling words from a list.
        Words will be glued by space character.
        :param slicing:
        :returns: String with joined words from finished_words
        """
        words = self.finished_words[slicing]
        return words if not words.__len__() > 1 else " ".join(words)

    def get_last_word(self) -> str:
        return self.get_words(slicing=slice(-1, None, None))

    def count_last_word_length(self, count_additional_space=True) -> int:
        """
        Count last finished word length.
        :param count_additional_space:
        :return:
        """
        last_word_length = self.finished_words[-1].__len__()
        return last_word_length + 1 if count_additional_space else last_word_length

    def clear_finished_words(self):
        """
        Clear finished_words list.
        :return:
        """
        self.finished_words.clear()

    def clear_queued_word(self):
        """
        Clear queued_word attribute.
        :return:
        """
        self.queued_word = ""
