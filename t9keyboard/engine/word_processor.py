from dataclasses import dataclass, field
from typing import List


@dataclass
class WordProcessor:
    finished_words: List[str] = field(default_factory=list)
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

    def finish_queued_word(self):
        """
        Append actual queued_word value to finished_words. Clear queued_word.
        :return: None
        """
        self.finished_words.append(self.queued_word)
        self.clear_queued_word()

    def get_words(self, slicing: slice = slice(0, None)) -> str:
        """
        Method for pulling words from a list.
        Words will be glued by space character.
        :param slicing:
        :returns: String with joined words from finished_words
        """
        words = self.finished_words[slicing]
        if words:
            return words[0] if not words.__len__() > 1 else " ".join(words)
        return ""

    def get_last_word(self) -> str:
        return self.get_words(slicing=slice(-1, None, None))

    def count_last_word_length(self, count_additional_space=True) -> int:
        """
        Count last finished word length.
        :param count_additional_space:
        :return:
        """
        try:
            last_word_length = self.finished_words[-1].__len__()
            return last_word_length + 1 if count_additional_space else last_word_length
        except IndexError:
            print("Finished words list is empty. Cannot count last word length.")

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

    def clear_word_processor_fields(self):
        """
        Method combining clearing queued_word and finished_words
        :return:
        """
        self.clear_finished_words()
        self.clear_queued_word()


# TODO: Convert this code sample into unit test
# word_processor = WordProcessor()
#
# word_processor.append_characters("cat")
# queue_value = word_processor.queued_word  # cat
# word_processor.finish_queued_word()
# print(word_processor.get_words())  # cat
#
# characters = ["d", "o", "g"]
# for character in characters:
#     word_processor.append_characters(character)
# word_processor.finish_queued_word()
# print(word_processor.get_last_word())  # dog
#
# print(word_processor.get_words(slicing=slice(1)))  # cat
# print(word_processor.get_words(slicing=slice(2)))  # "cat dog"
# word_processor.clear_word_processor_fields()
# print(word_processor.get_words())  # ""
# x = word_processor.count_last_word_length() # raise exception
